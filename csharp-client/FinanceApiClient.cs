using System.Net.Http.Json;
using CSharpClient.Models;

namespace CSharpClient;

public sealed class FinanceApiClient
{
    private readonly HttpClient _httpClient;

    public FinanceApiClient(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<FinanceAskResponse> AskAsync(FinanceAskRequest request, CancellationToken cancellationToken)
    {
        using HttpResponseMessage response = await _httpClient.PostAsJsonAsync(
            "/api/v1/finance/ask",
            request,
            cancellationToken);

        response.EnsureSuccessStatusCode();

        FinanceAskResponse? result = await response.Content.ReadFromJsonAsync<FinanceAskResponse>(
            cancellationToken: cancellationToken);

        return result ?? throw new InvalidOperationException("The API returned an empty response.");
    }
}
