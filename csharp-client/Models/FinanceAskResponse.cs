using System.Text.Json.Serialization;

namespace CSharpClient.Models;

public sealed record FinanceAskResponse(
    [property: JsonPropertyName("correlationId")] string CorrelationId,
    [property: JsonPropertyName("answer")] string Answer,
    [property: JsonPropertyName("blocked")] bool Blocked);
