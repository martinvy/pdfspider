## Nájdenie a stiahnutie odovzdávaných správ výskumných projektov

Program je určený pre sťahovanie dokumentov z webových stránok, konkrétne pre sťahovanie 
správ výskumných projektov.
 
Projekt pozostáva z dvoch súborov, pričom jeden z nich obsahuje kód grafického užívateľského 
rozhrania vytvoreného pomocou modulu tkinter. Druhý súbor obsahuje implementáciu automatického 
prechádzania všetkými odkazmi, ktoré boli nájdené na hlavnej stránke špecifikovanej adresou URL.
Odkazy, ktoré ukazujú na iné stránky sú ignorované.

Ak je nájdený odkaz na súbor vo formáte **pdf**, **doc** alebo **docx**, tak je tento odkaz spolu
s patričnými údajmi uložený do zoznamu výsledkov. Pri spustení aplikácie cez terminál
je možné špecifikovať, či budú tieto súbory stiahnuté z webovej stránky. V opačnom prípade
je výsledkom len zoznam nájdených odkazov. Pri použití GUI je možné zvoliť požadovaný
dokument a následne ho stiahnuť. Taktiež je možné stiahnuť všetky nájdené dokumenty.

Stiahnuté súbory každej webovej stránky sú uložené v ceste **downloads/**, kde je
vytvorený adresár danej webstránky. Takáto štruktúra je použitá aj pre zobrazenie
výsledkov v GUI.

