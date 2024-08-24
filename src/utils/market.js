import SteamMarketFetcher from "steam-market-fetcher";
import {parseMarketActivity} from "./parseMarketActivity.js";
const market = new SteamMarketFetcher({
  currency: "USD",
  format: "json",
});

export const fetch_data = async (item) => {
    try {
    const html_activity = await market.getItemActivity({
        item_nameid: item.item_nameid,
      });
      const data = parseMarketActivity(html_activity);
      return data
    } catch (error) {
      console.error("Error al obtener o procesar los datos:", error);
    }
  };