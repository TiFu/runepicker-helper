import { LCUClient, Page} from './LCUClient'

export interface PerkPage {
    id: number;
    primaryStyleId: number;
    selectedPerkIds: Array<number>;
    subStyleId: number;
    name: string;
}

export class LCUService {

    constructor(private client: LCUClient) {

    }

    /**
     * IF AVAILABLE IN CURRENT DISTRIBUTION
     */
    public isAvailable(): boolean {
        return this.client.isAvailable();
    }

    public isConnected(): boolean {
        return this.client.isConnected();
    }

    /**
     * Check if another empty page is available
     */
    public isEmptyPageAvailable(): Promise<boolean> {
        let maxPages = this.client.getMaxPages();
        let pages = this.getDeleteablePages();
        return Promise.all([maxPages, pages]).then((result: [number, PerkPage[]]) => {
            return result[1].length < result[0]; // minus default pages
        });
    }

    /**
     * Get pages for deletion? Maybe ask user
     */
    public getPages(): Promise<Array<PerkPage>> {
        return this.client.getPages();
    }

    /**
     * returns non default pages
     */
    public getDeleteablePages(): Promise<Array<PerkPage>> {
        return this.client.getPages().then((pages) =>{ 
            return pages.filter((e) => e.isDeletable);
        })
    }

    /**
     * in this case: save the currentPage and offer restore later?
     * @returns new created page
     */
    public replacePage(currentPage: PerkPage, newPage: PerkPage): Promise<PerkPage> {
        return this.client.deletePage(currentPage.id).then((): Promise<PerkPage> => {
            return this.client.createPage(this.perkPageToPage(newPage));
        }).then((page) => {
            console.log("Created new page: " + page.id);
            return this.client.selectPage(page.id).then(() => page);
        });
    }

    private perkPageToPage(page: PerkPage): Page {
        return {
            id: 0,
            current: true,
            isActive: true,
            isDeletable: true,
            isEditable: true,
            isValid: true,
            name: page.name,
            order: 0,
            primaryStyleId: page.primaryStyleId,
            selectedPerkIds: page.selectedPerkIds,
            subStyleId: page.subStyleId
        }
    }

    /**
     * Create a new rune page and return it (with the id set)
     * @param page configuration of the input page, returns created page
     */
    public createAndSetPage(page: PerkPage): Promise<PerkPage> {
        return this.client.createPage(this.perkPageToPage(page)).then((page) => {
            return this.client.selectPage(page.id).then(() => page);
        });
    }
}