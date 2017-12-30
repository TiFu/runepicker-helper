let fs = require('fs');
file = fs.readFileSync("src/environments/environment.prod.template.ts");
content = file.toString();
if(fs.existsSync("electron/dist")){
  console.log("Electron has been build");
  for(file of fs.readdirSync("electron/dist")){
    if(file.endsWith(".exe")){
      console.log("Found electron artifact:", file);
      content = content.replace(/electronDownloadPath: ".*"/, 'electronDownloadPath: "/' + file + '"');
    }
  }
}
console.log("Creating environment.prod.ts")
fs.writeFileSync("src/environments/environment.prod.ts", content);
