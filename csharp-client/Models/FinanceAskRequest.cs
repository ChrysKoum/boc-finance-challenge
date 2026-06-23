using System.Text.Json.Serialization;

namespace CSharpClient.Models;

public sealed record FinanceAskRequest(
    [property: JsonPropertyName("correlationId")] string CorrelationId,
    [property: JsonPropertyName("question")] string Question);
