
// // This sample uses the Apache HTTP client from HTTP Components (http://hc.apache.org/httpcomponents-client-ga/)
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.net.URI;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONObject;

public class Tagger {
	HttpClient httpclient = HttpClients.createDefault();
	HttpPost request;

	public Tagger() {
		try {
			URIBuilder builder = new URIBuilder("https://api.projectoxford.ai/vision/v1.0/analyze");
			builder.setParameter("visualFeatures", "Categories, Tags");
			builder.setParameter("language", "en");

			URI uri = builder.build();
			request = new HttpPost(uri);
			request.setHeader("Content-Type", "application/json");
			// Replace xxx with your key
			request.setHeader("Ocp-Apim-Subscription-Key", "xxx");
		} catch (Exception e) {
			System.out.println(e.getMessage());
		}
	}

	// Get the tags for an image at url, save image name, name in proper tag
	// file
	public void getTags(String url, String name) {
		try {
			StringEntity reqEntity = new StringEntity("{\"url\":\"" + url + "\"}");
			request.setEntity(reqEntity);
			HttpResponse response = httpclient.execute(request);
			HttpEntity entity = response.getEntity();

			if (entity != null) {
				// Parse information out of the json we get back
				String json = EntityUtils.toString(entity);
				JSONObject obj = new JSONObject(json);
				JSONArray tagArray = obj.getJSONArray("tags");
				for (int i = 0; i < tagArray.length(); i++) {
					JSONObject valueObject = tagArray.getJSONObject(i);
					String tag = valueObject.getString("name");
					double confidence = Double.parseDouble(valueObject.getString("confidence"));
					// We only take tags that are at or above 90% confidence
					if (confidence < 0.90) {
						break;
					}
					try {
						// Append our image to the proper tag file
						File f = new File(tag + ".csv");
						PrintWriter out = new PrintWriter(new FileWriter(f, true));
						out.append(name);
						out.append(",");
						out.close();
					} catch (Exception e) {
						System.out.println(e.getMessage());
					}
				}
			}
		} catch (Exception e) {
			System.out.println(e.getMessage());
		}

	}

	public static void main(String[] args) {
	}
}