const SteamMarketFetcher = require('steam-market-fetcher');
const fs = require('fs');
const market = new SteamMarketFetcher({
    currency: 'USD',
    format: 'json'
});

fs.readFile('./data/item_info.json', 'utf-8', (err, data) => {
    if (err) {
        console.log('Error reading file:', err);
    } else {
        console.log('Data read successfully');
        const itemData = JSON.parse(data).item_nameid;
        const fetch_data = async () => {
            try {
                const html_activity = await market.getItemActivity({ item_nameid: itemData });
                const data = parseMarketActivity(html_activity);
                fs.writeFile('data.json', JSON.stringify(data, null, 2), (err) => {
                    if (err) {
                        console.error('Error al escribir en el archivo:', err);
                    } else {
                        console.log('Archivo JSON creado exitosamente');
                    }
                });
            } catch (error) {
                console.error('Error al obtener o procesar los datos:', error);
            }
        }
        fetch_data()
    }
});

function parseMarketActivity(activityData) {
    const activities = activityData.activity;
    const parsedActivities = activities.reduce((accumulator, activity) => {
        let action;
        let price_USD;

        if (activity.includes('listed this item for sale')) {
            action = 'listed';
            const match = activity.match(/for sale for \$([\d.]+)/);
            if (match) {
                price_USD = parseFloat(match[1]);
            }
        } else if (activity.includes('purchased this item')) {
            action = 'purchased';
            const match = activity.match(/for \$([\d.]+)/);
            if (match) {
                price_USD = parseFloat(match[1]);
            }
        }

        if (action) {
            accumulator.push({ action, price_USD, used : false });
        }

        return accumulator;
    }, []);

    const date = new Date(activityData.timestamp * 1000);

    return {
        "success": activityData.success,
        "activities": parsedActivities,
        "date": date,
        "timestamp": activityData.timestamp
    };
}