import { dirname, join} from "path";
import { fileURLToPath } from "url";
import { fetch_data } from "./utils/market.js";
import fs from "fs";

const app = async (item) => {
  try{
    const data = await fetch_data(item);
    fs.writeFile(join(__dirname, 'data/data.json'), JSON.stringify(data, null, 2), (err) => {
      if (err) {
        console.error("Error al escribir en el archivo:", err);
        return;
      } 
      console.log(data)
      console.log("Archivo guardado correctamente");
    });  
  } catch (error) {
    console.error("No se puedo obtener la data:", error);
  }
}

const __dirname = dirname(fileURLToPath(import.meta.url));
fs.readFile(join(__dirname, './data/item_info.json'), 'utf8', (err, data) => {
  const item = JSON.parse(data);
  app(item);
})