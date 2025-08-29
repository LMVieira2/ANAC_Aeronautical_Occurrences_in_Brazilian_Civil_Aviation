# Problem with downloading the CSV Files

When attempting to download the CSV file directly via Python (requests or cloudscraper), we receive an HTTP 403 Forbidden error.

## Cause

The site dedalo.sti.fab.mil.br is protected by Cloudflare, which implements security challenges to prevent automated access. This protection works as follows:

When a browser accesses the site, Cloudflare executes a JavaScript challenge to verify that the user is human.

Only after passing this challenge the browser can access the CSV file.

Libraries like requests or cloudscraper do not execute JavaScript, so any direct request is blocked, resulting in HTTP 403.

### Specifically for the download button:

It sends a POST request to https://dados.gov.br/api/publico/recurso/registrar-download.

This POST registers the download, and the browser receives temporary cookies and tokens required to access the file.

Without executing Cloudflare’s JavaScript, the server does not allow file access, and any direct download attempt fails.

## Consequence

It is not possible to download the CSV directly with plain Python. Any attempt using requests, cloudscraper, or urllib will result in 403 Forbidden.

## Possible Solutions

### Manual download:

Click the download button on the site and save the CSV locally.

Then load the file into Spark:

df = spark.read.option("header", True)\
               .option("sep", ";")\
               .csv("/dbfs/FileStore/tables/{table_Name}.csv")\
df.createOrReplaceTempView("recommendation")


### Automation via real browser:

Use Selenium or Playwright to open the site, click the button, and save the file automatically.

This works because a real browser can pass Cloudflare’s JavaScript challenge.

###💡 Note: 
Methods that do not execute JavaScript (requests, cloudscraper) will not work in this case due to Cloudflare’s advanced protection.