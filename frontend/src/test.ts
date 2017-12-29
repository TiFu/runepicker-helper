import {LCUClientImpl} from './electron/LCUClientImpl'
import {Page} from './core/LCUClient'

let impl = new LCUClientImpl(() => {
    impl.getPages().then((pages) => {
        let p: Page = {
            id: 5,
            current: true,
            isActive: true,
            isDeletable: true,
            isEditable: true,
            isValid: true,
            name: "Test",
            order: 0,
            primaryStyleId: 8400,
            selectedPerkIds: [
                8437, 8242, 8430, 8451, 8224, 8237
            ],
            subStyleId: 8200
        };
        return impl.createPage(p);
    }).then(() => {
        console.log("Selected Page");
    }).catch((err) => {
        console.log(err);
    })
}, () => {});
console.log("Trying to start connector");
