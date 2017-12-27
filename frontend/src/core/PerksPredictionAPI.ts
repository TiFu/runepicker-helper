import * as socketio from 'socket.io-client'

export interface PerksPredictionAPIListener {

    onConnect(): void;
    onDisconnect(): void;
    onReceivedPrimaryStyle(predictions: Response<PerkStylePrediction>): void;
    onReceivedSubStyle(predictions: Response<PerkStylePrediction>): void;
    onReceivedPrimaryPerks(prediction: Response<PerkPrediction>): void;
    onReceivedSubPerks(prediction:  Response<PerkPrediction>): void;
}

export interface CallResult {
    success: boolean; // true if no user error (i.e. the request is being processed, but might still fail)
    error?: string;
}

export interface Response<T> {
    success: boolean; // true if the data is present and T, false if failed with error message in data
    data: T | string;
}

export type PerkStyle = "8000" | "8100" | "8200" | "8300" | "8400"
export type Perks = string // TODO: could define all runes here

export interface PerkStylePrediction {
    "8000": number;
    "8100": number;
    "8200": number;
    "8300": number;
    "8400": number;
}

export interface PerkPrediction {
    [key: number]: number;
}

export type Lane = "MARKSMAN" | "SUPPORT" | "TOP" | "MIDDLE" | "JUNGLE";

export interface BaseChampionInformation {
    championId: number;
    lane: Lane;
}

export class PerksPredictionAPI {
    private socket: SocketIOClient.Socket;

    constructor(private url: string, private namespace: string = "/Perkprediction") {

    }

    public connect(listener: PerksPredictionAPIListener): void {
        this.socket = socketio.connect(this.url + this.namespace);
        this.socket.on("connect", () => listener.onConnect());
        this.socket.on("disconnect", () => listener.onDisconnect())

        this.socket.on("primaryStyles", (data: Response<PerkStylePrediction>) => listener.onReceivedPrimaryStyle(data));
        this.socket.on("subStyles", (data: Response<PerkStylePrediction>) => listener.onReceivedSubStyle(data));
        this.socket.on("primaryRunes", (perks: Response<PerkPrediction>) => listener.onReceivedPrimaryPerks(perks));
        this.socket.on("subRunes", (perks: Response<PerkPrediction>) => listener.onReceivedSubPerks(perks));
        this.socket.open();
    }

    public close(): void {
        this.socket.close();
    }

    public startPrediction(data: BaseChampionInformation): Promise<CallResult> {
        return new Promise<CallResult>((resolve, reject) => {
            this.socket.emit("startPrediction", data, function(result: CallResult) {
                if (result.success) {
                    resolve(result);
                } else {
                    reject(result);
                }
            } )
        });
    }

    public selectPrimaryStyle(style: PerkStyle): Promise<CallResult> {
        return this.sendRequest("selectPrimaryStyle", style);       
    }

    public selectSubStyle(style: PerkStyle): Promise<CallResult> {
        return this.sendRequest("selectSubStyle", style);              
    }

    public selectPrimaryRunes(runes: Array<Perks>): Promise<CallResult> {
        return this.sendRequest("selectPrimaryRunes", runes); 
    }  
    
    private sendRequest(event: string, data: any): Promise<CallResult> {
        return new Promise<CallResult>((resolve, reject) => {
            this.socket.emit(event, data, function(result: CallResult) {
                if (result.success) {
                    resolve(result);
                } else {
                    reject(result);
                }
            } )
        });                
        
    }
}