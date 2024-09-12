import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import createDebugMessages from 'debug';
import { convert } from 'html-to-text';
import axios from 'axios';
import md5 from 'md5';
import * as cheerio from 'cheerio';

import { BaseLoader } from '../interfaces/base-loader.js';
import { cleanString, truncateCenterString } from '../util/strings.js';

export class WebLoader extends BaseLoader<{ type: 'WebLoader' }> {
    private readonly debug = createDebugMessages('maap:loader:WebLoader');
    private readonly contentOrUrl: string;
    private readonly isUrl: boolean;
    private readonly subpages: number;

    constructor({}: { url: string; chunkSize?: number; chunkOverlap?: number, subpages?: number });
    constructor({}: { content: string; chunkSize?: number; chunkOverlap?: number, subpages?: number });
    constructor({
        content,
        url,
        chunkSize,
        chunkOverlap,
        subpages,
    }: {
        content?: string;
        url?: string;
        chunkSize?: number;
        chunkOverlap?: number;
        subpages?: number;

    }) {
        super(`WebLoader_${md5(content ? `CONTENT_${content}` : `URL_${url}`)}`, chunkSize ?? 2000, chunkOverlap ?? 0);

        this.isUrl = !content;
        this.subpages = subpages ? subpages : 0;
        this.contentOrUrl = content ?? url;
    }

    override async *getUnfilteredChunks() {
        const chunker = new RecursiveCharacterTextSplitter({
            chunkSize: this.chunkSize,
            chunkOverlap: this.chunkOverlap,
        });

        try {
            const data = this.isUrl
                ? (await axios.get<string>(this.contentOrUrl, { responseType: 'document' })).data
                : this.contentOrUrl;

            if(this.subpages > 0){
                // search for links
                const html = cheerio.load(data);
                let links = [];

                html("a").each((_i, value) => {
                    let link = html(value).attr("href");
                    if( link.includes("unibas")){
                        links.push(link)
                    }
                })

                for (let link of links) {
                    console.log("🆕LOADING Subpage: " + link)
                    const webLoader = new WebLoader({ url:link, chunkSize: this.chunkSize, chunkOverlap: this.chunkOverlap, subpages: this.subpages - 1 });

                    for await (const chunk of webLoader.getUnfilteredChunks()) {
                        yield {
                            ...chunk,
                            metadata: {
                                ...chunk.metadata,
                                type: <'JsonCollectionsLoader'>'JsonCollectionsLoader',
                                originalSource: link,
                            },
                        };
                    }
                }

            }

            const text = convert(data, {
                baseElements: {
                    selectors: ['section.content_block'],
                },
                wordwrap: false,
                preserveNewlines: false,
            }).replace(/(?:https?|ftp):\/\/[\n\S]+/g, '');

            const tuncatedObjectString = this.isUrl ? undefined : truncateCenterString(this.contentOrUrl, 50);

            const chunks = await chunker.splitText(cleanString(text));
            for (const chunk of chunks) {
                yield {
                    pageContent: chunk,
                    metadata: {
                        type: <'WebLoader'>'WebLoader',
                        source: this.isUrl ? this.contentOrUrl : tuncatedObjectString,
                    },
                };
            }
        } catch (e) {
            this.debug('Could not parse input', this.contentOrUrl, e);
        }
    }
}
