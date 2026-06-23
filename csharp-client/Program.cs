using CSharpClient;
using CSharpClient.Models;

string apiUrl = Environment.GetEnvironmentVariable("FINANCE_API_URL") ?? "http://localhost:8000";

using HttpClient httpClient = new()
{
    BaseAddress = new Uri(apiUrl),
    Timeout = TimeSpan.FromSeconds(5),
};

FinanceApiClient client = new(httpClient);

FinanceAskRequest request = new(
    CorrelationId: Guid.NewGuid().ToString(),
    Question: args.Length > 0 ? string.Join(' ', args) : "How do I save money?");

try
{
    FinanceAskResponse response = await client.AskAsync(request, CancellationToken.None);

    Console.WriteLine($"Correlation ID: {response.CorrelationId}");
    Console.WriteLine($"Blocked: {response.Blocked}");
    Console.WriteLine($"Answer: {response.Answer}");
}
catch (Exception ex) when (ex is HttpRequestException or TaskCanceledException or InvalidOperationException)
{
    Console.WriteLine($"Request failed: {ex.Message}");
}
