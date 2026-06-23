FROM mcr.microsoft.com/dotnet/sdk:8.0

WORKDIR /app

COPY csharp-client.csproj .
RUN dotnet restore

COPY . .

CMD ["dotnet", "run", "--no-restore"]
