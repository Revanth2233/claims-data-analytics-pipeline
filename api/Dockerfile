FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ClaimsAnalytics.API/ClaimsAnalytics.API.csproj ClaimsAnalytics.API/
RUN dotnet restore ClaimsAnalytics.API/ClaimsAnalytics.API.csproj
COPY ClaimsAnalytics.API/ ClaimsAnalytics.API/
RUN dotnet publish ClaimsAnalytics.API/ClaimsAnalytics.API.csproj -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/publish .
RUN mkdir -p logs
EXPOSE 8080
ENTRYPOINT ["dotnet", "ClaimsAnalytics.API.dll"]
