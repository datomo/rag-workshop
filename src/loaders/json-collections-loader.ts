import md5 from 'md5';

import { BaseLoader } from '../interfaces/base-loader.js';
import { getTextExtractor } from 'office-text-extractor';
import { WebLoader } from './web-loader.js';
import { PdfLoader } from './pdf-loader.js';
import { SitemapLoader } from './sitemap-loader.js';

export class JsonCollectionsLoader extends BaseLoader<{ type: 'JsonCollectionsLoader' }> {
    private readonly url: string;

    constructor({ url, chunkSize, chunkOverlap }: { url: string; chunkSize?: number; chunkOverlap?: number }) {
        super(`SitemapLoader_${md5(url)}`, chunkSize ?? 2000, chunkOverlap);
        this.url = url;
    }

    override async *getUnfilteredChunks() {
        const extractor = getTextExtractor();
        const docxParsed = await extractor.extractText({ input: this.url, type:  'file' });

        const sites = JSON.parse(docxParsed).links
        console.log(sites)

        for (const url of (sites as any[])) {
            let adjustedUrl = "";
            let withSubpages = false;
            if( typeof url === 'string' ){
               adjustedUrl = url as string;
            }else{
                adjustedUrl = url.link;
                withSubpages = url.subpages;
            }
            adjustedUrl = adjustedUrl;
            let msg = "🆕LOADING";
            if (withSubpages) {
                msg += " with subpages"
            }
            msg += `: ${adjustedUrl}`;
            console.log(msg)


            if( adjustedUrl.toLowerCase().endsWith(".xml")){
                const sitemapLoader = new SitemapLoader({ url, chunkSize: this.chunkSize, chunkOverlap: this.chunkOverlap });

                for await (const chunk of sitemapLoader.getUnfilteredChunks()) {
                    yield {
                        ...chunk,
                        metadata: {
                            ...chunk.metadata,
                            type: <'JsonCollectionsLoader'>'JsonCollectionsLoader',
                            originalSource: this.url,
                        },
                    };
                }
            }else if( adjustedUrl.toLowerCase().endsWith(".pdf")){
                const pdfLoader = new PdfLoader({ url, chunkSize: this.chunkSize, chunkOverlap: this.chunkOverlap });

                for await (const chunk of pdfLoader.getUnfilteredChunks()) {
                    yield {
                        ...chunk,
                        metadata: {
                            ...chunk.metadata,
                            type: <'JsonCollectionsLoader'>'JsonCollectionsLoader',
                            originalSource: this.url,
                        },
                    };
                }
            }else{
                try {
                    const webLoader = new WebLoader({
                        url: adjustedUrl,
                        chunkSize: this.chunkSize,
                        chunkOverlap: this.chunkOverlap,
                        withSubpages
                    });

                    for await (const chunk of webLoader.getUnfilteredChunks()) {
                        yield {
                            ...chunk,
                            metadata: {
                                ...chunk.metadata,
                                type: <'JsonCollectionsLoader'>'JsonCollectionsLoader',
                                originalSource: this.url,
                            },
                        };
                    }
                }catch (error) {
                    console.log("Could not load: " + adjustedUrl);
                }
            }
        }
    }
}
