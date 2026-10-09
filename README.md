# gabiknits-www

Strona aplikacji Gabi Knits (docelowo https://gabiknits.app), publikowana przez GitHub Pages.
Statyczna: bez skryptów, analityki i zewnętrznych zasobów. Kod aplikacji jest w osobnym, prywatnym repozytorium.

Strony główne (`index.html` i `pl|de|nb|da|sv/index.html`) składa `python3 generuj.py`: teksty w sześciu
językach są w `teksty.py`, układ i ręcznie rysowane ikony SVG w `generuj.py`, wygląd w `assets/site.css`
(jasny i ciemny motyw, od 360 do 1440 px). Zrzuty aplikacji leżą w `assets/shots/<język>/` (eink, phone, tablet,
step1–3 .png); brakujące zastępują szkice z `assets/shots/_szkic/`, więc po dodaniu zrzutów wystarczy
ponownie uruchomić generator. Polityka prywatności (`privacy/`, `xx/privacy/`) jest pisana ręcznie
(`assets/doc.css`) - generator podmienia w niej tylko przełącznik języków.

Krój Prata - licencja SIL Open Font License, `assets/Prata-OFL.txt`.
