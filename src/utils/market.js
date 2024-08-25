import SteamMarketFetcher from "steam-market-fetcher";
import {parseMarketActivity} from "./parseMarketActivity.js";
const market = new SteamMarketFetcher({
  currency: "USD",
  format: "json",
});

export const fetch_data = async (item) => {
  while (true) {
      try {
          const html_activity = await market.getItemActivity({
              item_nameid: item.item_nameid,
          });
          const data = parseMarketActivity(html_activity);
          return data;  // Si la petición es exitosa, salimos del bucle y devolvemos los datos
      } catch (error) {
          console.error("Error al obtener o procesar los datos:", error);
          console.log("Reintentando...");
          await new Promise(resolve => setTimeout(resolve, 2000)); // Espera 2 segundos antes de reintentar
      }
  }
};