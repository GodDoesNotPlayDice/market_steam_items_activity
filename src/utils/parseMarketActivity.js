export const parseMarketActivity = (activityData) => {
    const activities = activityData.activity;
    const parsedActivities = activities.reduce((accumulator, activity) => {
      let action;
      let price_USD;
  
      if (activity.includes("Listed for sale")) {
        action = "listed";
        const match = activity.match(/\$([\d.]+)/);
        if (match) {
          price_USD = parseFloat(match[1]);
        }
      } else if (activity.includes("Purchased")) {
        action = "purchased";
        const match = activity.match(/\$([\d.]+)/);
        if (match) {
          price_USD = parseFloat(match[1]);
        }
      }
  
      if (action) {
        accumulator.push({ action, price_USD, used: false });
      }
  
      return accumulator;
    }, []);
  
    const date = new Date(activityData.timestamp * 1000);
  
    return {
      success: activityData.success,
      activities: parsedActivities,
      date: date,
      timestamp: activityData.timestamp,
    };
  }
