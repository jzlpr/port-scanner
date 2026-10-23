Sammanfattning av koden

Den här Python-koden är ett interaktivt nätverksscannerverktyg som används för att ta reda på vilka portar som är öppna på en specifik dator, server eller nätverksenhet. Den bygger på det kraftfulla skanningsverktyget Nmap via Python-biblioteket nmapthon2.
Så här fungerar det i praktiken:

1. Användarindata:
    Skriptet startar med att fråga dig (användaren) om två saker:
    Mål: Vilken IP-adress eller domän du vill skanna (standard är 192.168.1.1).
    Portintervall: Vilka portar som ska undersökas (standard är de vanligaste portarna 1-1024).

2. Skanning med Nmap:
    Skriptet använder Nmap för att skicka nätverksförfrågningar till målet med en optimerad hastighet (-T4).

3. Snygg presentation av resultatet:
    När skanningen är klar filtrerar skriptet bort stängda portar och visar en ren tabell över:
    Vilka portar som är öppna (t.ex. 80/tcp).
    Vilken status de har (open).
    Vilken tjänst som körs där (t.ex. http, ssh).

4. Felhantering:
    Om något går fel (till exempel om Nmap inte är installerat på datorn eller om målet inte svarar) fångar skriptet upp felet och visar ett tydligt felmeddelande i stället för att krascha.

- Användningsområden

    Skriptet är perfekt för nätverksadministration, grundläggande säkerhetskontroller (penetrationstestning) eller för att felsöka vilka tjänster som är tillgängliga på en lokal server.
