# Bilibili_Dataset
*Note some bullet comments file may be missing during 20240824 and 20240901, since the "Star Dome Railway Summer Festival" is happening during this time interval, and it is hard to filter those videos out.

This publicly available dataset includes the daily top 100 video details from the Chinese video platform bilibili.com. It includes video titles, uploaders, view counts, comment sections, popular comments, descriptions, and, when available, AI summaries. 

Feel free to fork this repository to create datasets for other social media platforms like Weibo, Douyin, RED, and Twitter.
I used a webdriver from the selenium package (simply run pip install selenium in terminal) because some websites use JavaScript to dynamically load content after the initial HTML is loaded. I used Safari WebDriver. However, for Windows users, it is necessary to change to webdriver to ChromeDriver or Microsoft Edge WebDriver to scrape the websites.

