using System.Net.Http.Headers;
using System.Text.Json;
using System.Text.Json.Serialization;

Console.Write("Enter Query: ");

var Query = Console.ReadLine();

var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Post,
    RequestUri = new Uri("https://chatgpt-api8.p.rapidapi.com/"),
    Headers =
    {
        //Insert API Key for https://rapidapi.com/haxednet/api/chatgpt-api8/
        { "X-RapidAPI-Key", "API KEY" },
        { "X-RapidAPI-Host", "chatgpt-api8.p.rapidapi.com" },
    },
    Content = new StringContent("[\r{\r\"content\": \"" + Query + "\",\r\"role\": \"user\"\r}\r]")
	{
		Headers =
		{
			ContentType = new MediaTypeHeaderValue("application/json")
		}
	}
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    string body = await response.Content.ReadAsStringAsync();
    var answer = System.Text.Json.JsonDocument.Parse(body).RootElement.GetProperty("text");
    Console.WriteLine(answer);
}