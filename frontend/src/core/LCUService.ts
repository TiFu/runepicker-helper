import { LCUClient, Page} from './LCUClient'

export interface PerkPage {
    id: number;
}

export class LCUService {

    constructor(private client: LCUClient) {

    }

    /**
     * Check if another empty page is available
     */
    public isEmptyPageAvailable(): Promise<boolean> {
        let maxPages = this.client.getMaxPages();
        let pages = this.client.getPages();
        return Promise.all([maxPages, pages]).then((result: [number, Page[]]) => {
            return result[1].length < result[0];
        });
    }

    /**
     * Get pages for deletion? Maybe ask user
     */
    public getPages(): Promise<Array<PerkPage>> {
        return this.client.getPages();
    }
    
    /**
     * in this case: save the currentPage and offer restore later?
     */
    public replacePage(currentPage: PerkPage, newPage: PerkPage): Promise<PerkPage> {
        return this.client.deletePage(currentPage.id).then((result): Promise<PerkPage> => {
            return this.client.createPage(newPage);
        });
    }

    /**
     * Create a new rune page and return it (with the id set)
     * @param page configuration of the input page
     */
    public createAndSetPage(page: PerkPage): Promise<PerkPage> {
        return this.client.createPage(page);
    }
}