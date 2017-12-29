import {LCUClientImpl} from './electron/LCUClientImpl'
import {Page} from './core/LCUClient'
import {LCUService, PerkPage} from './core/LCUService'

let pOld: Page = {
    id: 265242205,
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

let pNew: Page = {
    id: 5,
    current: true,
    isActive: true,
    isDeletable: true,
    isEditable: true,
    isValid: true,
    name: "My replaced page",
    order: 0,
    primaryStyleId: 8400,
    selectedPerkIds: [
        8437, 8242, 8430, 8451, 8224, 8237
    ],
    subStyleId: 8200
};


let impl = new LCUClientImpl(() => {
     let service = new LCUService(impl);
     console.log(impl.isConnected());
     service.isEmptyPageAvailable().then((available) => {
         console.log("Empty available: " + available);
        return service.createAndSetPage(pOld);
     }).then((page: PerkPage) => {
        return service.replacePage(page, pNew);
     }).then((createdPage) => {
        console.log(createdPage);
        impl.disconnect();
     }).catch((err) => {
         console.log(err.body);
     })
}, () => { console.log("disconnected"); process.exit()});

console.log("Trying to start connector");
