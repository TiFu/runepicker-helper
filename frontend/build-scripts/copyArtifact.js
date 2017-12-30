let fs = require('fs');
if(fs.existsSync("electron/dist")){
  for(file of fs.readdirSync("electron/dist")){
    if(file.endsWith(".exe")){
      console.log("Found electron artifact", file)
      console.log("Copying artifact")
      fs.createReadStream('electron/dist/' + file).pipe(fs.createWriteStream('dist/' + file));
    }
  }
}
