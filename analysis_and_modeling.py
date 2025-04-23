import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load the dataset
df = pd.read_csv("final_dataset_with_weather.csv", parse_dates=["Date"])

# Preprocessing
df["Weather_Rain"] = df["WeatherConditions"].str.contains("Rain", case=False).astype(int)

# --- EDA ---

# Histograms
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.hist(df["ScreenTimeHours"], bins=10, color="skyblue", edgecolor="black")
plt.title("Screen Time Distribution")
plt.xlabel("Hours")

plt.subplot(1, 2, 2)
plt.hist(df["SocialProxy"], bins=10, color="salmon", edgecolor="black")
plt.title("Social Activity Proxy Distribution")
plt.xlabel("Ping Count")
plt.tight_layout()
plt.savefig("final_eda_histograms1.png")

# Scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(df["ScreenTimeHours"], df["SocialProxy"], alpha=0.7, color="orange")
plt.title("Screen Time vs Social Activity Proxy")
plt.xlabel("Screen Time (Hours)")
plt.ylabel("Ping Count")
plt.grid(True)
plt.tight_layout()
plt.savefig("xtended_screen_vs_social.png")

# Time series plot
plt.figure(figsize=(12, 6))
plt.plot(df["Date"], df["ScreenTimeHours"], label="Screen Time", color="orange")
plt.plot(df["Date"], df["SocialProxy"] / 60, label="Social Proxy (scaled)", color="green")
plt.legend()
plt.title("Daily Screen Time & Social Activity")
plt.xlabel("Date")
plt.ylabel("Hours / Ping Proxy")
plt.grid(True)
plt.tight_layout()
plt.savefig("fscreen_social_timeseries.png")

# Weather condition bar chart
df["MainWeather"] = df["WeatherConditions"].str.extract(r"(\w+)")
weather_counts = df["MainWeather"].value_counts()
plt.figure(figsize=(10, 6))
weather_counts.plot(kind="bar", color="cornflowerblue", edgecolor="black")
plt.title("Weather Condition Frequency")
plt.xlabel("Weather Type")
plt.ylabel("Number of Days")
plt.tight_layout()
plt.savefig("fweather_condition_frequency.png")

# Daily weather bar timeline
daily_weather = df.groupby("Date")["MainWeather"].first()
color_map = {
    "Clear": "gold", "Rain": "skyblue", "Cloudy": "lightgray",
    "Partially": "orange", "Overcast": "dimgray", "Snow": "white", "Fog": "lightgreen"
}
bar_colors = daily_weather.map(lambda w: color_map.get(w, "lightsteelblue"))
plt.figure(figsize=(14, 6))
plt.bar(daily_weather.index, [1]*len(daily_weather), color=bar_colors, edgecolor="black")
plt.title("Daily Weather Conditions")
plt.xticks(rotation=45)
plt.yticks([])
plt.tight_layout()
plt.savefig("fdaily_weather_conditions_histogram.png")

# --- Machine Learning ---

# Features and target
X = df[["ScreenTimeHours", "Weather_Rain"]]
y = df["SocialProxy"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)

print("Model Performance:")
print("Test MSE:", round(mse, 2))
print("Train R²:", round(model.score(X_train, y_train), 2))
