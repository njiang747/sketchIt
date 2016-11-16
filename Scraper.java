import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URI;
import java.net.URL;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONObject;

public class Scraper {
	public static void main(String[] args) throws Exception {

		HttpClient httpclient = HttpClients.createDefault();
		// Here lie the queries we have already included in our database: "cat",
		// "cake", "house", "heart", "moon", "chair", "tree",
		// "eiffel tower", "mountain", "computer", "mouese", "bag", "headshot",
		// "pyramid", "star", "guitar", "boat", "car", "dog", "flower",
		// "statue", "pencil",
		// "water bottle", "cards", "chicken", "bicycle", "night sky", "cresent
		// moon", "new york skyline", "ladybug", "spongebob", "pikachu",
		// "apple",
		// "banana", "money", "ball", "donut",
		// "food", "pets", "landscape", "Snorelax"
		// "pants", "socks", "lamp", "table", "sun"

		// Input search queries inside this array
		String[] queries = {};

		// Create a new Tagger object so we can tag
		Tagger t = new Tagger();
		try {
			URIBuilder builder = new URIBuilder("https://api.cognitive.microsoft.com/bing/v5.0/images/search");
			builder.setParameter("count", "200");
			builder.setParameter("offset", "0");
			builder.setParameter("mkt", "en-us");
			builder.setParameter("safeSearch", "Moderate");
			for (int j = 0; j < queries.length; j++) {
				// Replace path with where you want to save your images
				String folderPath = "C:\\Users\\jonfu\\workspace\\BingImages\\images2\\" + queries[j];
				// Path for use on Mac systems
				String relativeMacFolderPath = "/images/" + queries[j];
				File file = new File(folderPath);
				if (!file.exists()) {
					if (file.mkdir()) {
						System.out.println("Directory is created!");
					} else {
						System.out.println("Failed to create directory!");
					}
				}

				builder.setParameter("q", queries[j]);

				URI uri = builder.build();
				HttpGet request = new HttpGet(uri);
				// Replace xxx with your key
				request.setHeader("Ocp-Apim-Subscription-Key", "xxx");

				HttpResponse response = httpclient.execute(request);
				HttpEntity entity = response.getEntity();

				if (entity != null) {
					// Parse out information from the JSON we get back
					String json = EntityUtils.toString(entity);
					JSONObject obj = new JSONObject(json);
					JSONArray valueArray = obj.getJSONArray("value");
					for (int i = 0; i < valueArray.length(); i++) {

						JSONObject valueObject = valueArray.getJSONObject(i);
						String url = valueObject.getString("thumbnailUrl");
						System.out.println(i);
						t.getTags(url, relativeMacFolderPath + "/image" + i + ".jpg");
						saveImage(url, folderPath + "\\image" + i + ".jpg");
					}
				}
			}

		} catch (Exception e) {
			System.out.println("ERROR");
			System.out.println(e.getMessage());
		}
	}

	// Save an image from a url, imageUrl, to path, destinationFile
	public static void saveImage(String imageUrl, String destinationFile) throws IOException {
		URL url = new URL(imageUrl);
		InputStream is = url.openStream();
		OutputStream os = new FileOutputStream(destinationFile);

		byte[] b = new byte[2048];
		int length;

		while ((length = is.read(b)) != -1) {
			os.write(b, 0, length);
		}

		is.close();
		os.close();
	}

}
