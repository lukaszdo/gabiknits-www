#!/usr/bin/env python3
"""Generator stron głównych Gabi Knits w sześciu językach.

Teksty są w słowniku T poniżej; układ w funkcji page(). Uruchomienie: `python3 generuj.py`
nadpisuje index.html (angielski, w korzeniu) i pl/, de/, nb/, da/, sv/index.html.
Polityka prywatności (privacy/, xx/privacy/) jest pisana ręcznie - generator jej nie rusza.
"""
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
LANGS = ["en", "pl", "de", "nb", "da", "sv"]
NAMES = {"en": "EN", "pl": "PL", "de": "DE", "nb": "NO", "da": "DA", "sv": "SV"}
COMPANY = "ŁUKASZ DOMAŃSKI IT ONE STUDIO"

# Flagi do wyboru języka - rysowane w SVG w treści strony (bez zewnętrznych plików).
# Angielski: flaga Wielkiej Brytanii.
FLAGS = {
    "en": '<svg viewBox="0 0 60 30"><clipPath id="uk"><path d="M0 0v30h60V0z"/></clipPath><g clip-path="url(#uk)">'
          '<path d="M0 0v30h60V0z" fill="#012169"/><path d="M0 0l60 30m0-30L0 30" stroke="#fff" stroke-width="6"/>'
          '<path d="M0 0l60 30m0-30L0 30" stroke="#C8102E" stroke-width="2.4"/><path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/>'
          '<path d="M30 0v30M0 15h60" stroke="#C8102E" stroke-width="6"/></g></svg>',
    "pl": '<svg viewBox="0 0 16 10"><path d="M0 0h16v5H0z" fill="#fff"/><path d="M0 5h16v5H0z" fill="#DC143C"/></svg>',
    "de": '<svg viewBox="0 0 5 3"><path d="M0 0h5v1H0z" fill="#000"/><path d="M0 1h5v1H0z" fill="#DD0000"/><path d="M0 2h5v1H0z" fill="#FFCE00"/></svg>',
    "nb": '<svg viewBox="0 0 22 16"><path d="M0 0h22v16H0z" fill="#BA0C2F"/><path d="M6 0h4v16H6zM0 6h22v4H0z" fill="#fff"/>'
          '<path d="M7 0h2v16H7zM0 7h22v2H0z" fill="#00205B"/></svg>',
    "da": '<svg viewBox="0 0 37 28"><path d="M0 0h37v28H0z" fill="#C8102E"/><path d="M12 0h4v28h-4zM0 12h37v4H0z" fill="#fff"/></svg>',
    "sv": '<svg viewBox="0 0 16 10"><path d="M0 0h16v10H0z" fill="#006AA7"/><path d="M5 0h2v10H5zM0 4h16v2H0z" fill="#FECC00"/></svg>',
}


def lang_nav(lang, href, label="Language"):
    """Przełącznik języków z flagami; [href] - adres strony w danym języku względem bieżącej."""
    items = []
    for l in LANGS:
        inner = f'<span class="flag" aria-hidden="true">{FLAGS[l]}</span><span>{NAMES[l]}</span>'
        if l == lang:
            items.append(f'<span class="cur" lang="{l}">{inner}</span>')
        else:
            items.append(f'<a href="{href(l)}" hreflang="{l}" lang="{l}">{inner}</a>')
    return f'<nav class="lang" aria-label="{label}">' + "".join(items) + "</nav>"
EMAIL = "contact@gabiknits.app"

T = {
    "en": dict(
        title="Gabi Knits – knitting chart reader for Android and BOOX e-ink",
        desc="Gabi Knits opens your PDF knitting patterns, finds the chart and guides you row by row. For Android phones, tablets and BOOX e-ink. No account, no ads.",
        nav=("How it works", "Features", "Price", "Questions", "Contact"),
        claim="Knit from your chart, row by row.",
        intro="Gabi Knits opens your PDF patterns, finds the chart on the page and clearly marks the row you are knitting. Your progress in every project is saved automatically.",
        soon="Coming soon to Google Play",
        devices="Android phones · tablets · BOOX e-ink tablets",
        pledge="No account · no ads · no tracking",
        shots=("BOOX e-ink tablet", "Phone", "Tablet"),
        # Opisy prawdziwych zrzutów - wrócą z nimi; na razie puste ilustracje (alt="").
        alt=("Gabi Knits on a BOOX e-ink tablet: a chart with the current row framed", "Gabi Knits on a phone: the current row highlighted in yellow", "Gabi Knits on a tablet in landscape: chart and row buttons side by side"),
        how_t="How it works", how_l="Three steps from a PDF to the needles.",
        steps=[("Open your pattern", "Add a PDF pattern as a project. It gets its own name and remembers where you stopped."),
               ("Tap the chart", "Gabi Knits finds the chart's frame and rows by itself. You can correct the edges if needed."),
               ("Knit row by row", "The current row is clearly marked. One big button takes you to the next row – easy with one hand.")],
        feat_t="What it can do", feat_l="Only what helps you finish the row – nothing that gets in the way.",
        feats=[("Several charts in one pattern", "Front, back and sleeves – each chart keeps its own row and history."),
               ("Switch charts with one tap", "A floating list, or a bar by the row counter that never covers the page."),
               ("The pattern key at hand", "Mark the symbol key once and open it over the page without losing your row."),
               ("The row follows you", "The chart can move under a fixed bar, so the current row stays in the middle of the screen."),
               ("Knitting timer", "See how long a project took – it runs only when you start it."),
               ("Six languages", "English, Polish, German, Norwegian, Danish and Swedish.")],
        eink_badge="Made for<br>e-ink", eink_t="Calm on e-ink",
        eink_p="Gabi Knits started on a BOOX Note Air. On e-ink it has no animations or colours that matter – black on white, large buttons and big row numbers you can read from your knitting. On phones and regular tablets it uses colour and smooth movement.",
        price_t="Price", price_l="Try everything free for 14 days. Then choose what suits you.",
        plans=[("Monthly", "€2.99", "per month", True), ("Yearly", "€5.99", "per year", True), ("Forever", "€14.99", "one-time payment", False)],
        best="Best value", trial_yes="<b>14 days free</b>, then renews automatically unless you cancel.", trial_no="Pay once, keep it for good.",
        price_note="One free trial per Google account. Prices are in euro; Google Play shows the price in your currency. Cancel any time in Google Play.",
        priv_t="Your patterns stay with you",
        priv_points=("No account", "No ads", "No tracking or analytics", "Works offline"),
        priv_p="Your PDF patterns, projects and row numbers stay on your device. The app uses the internet only to handle a purchase and check that you have access.",
        priv_link="Read the privacy policy",
        faq_t="Questions",
        faq=[("Do I need an account?", "No. There is no sign-up and no login. Purchases go through your Google Play account."),
             ("Does it work without internet?", "Yes. Reading and knitting never need the internet. A connection is needed only to buy and, now and then, to confirm your subscription."),
             ("Which devices does it run on?", "Android 8.1 or newer: phones, tablets and BOOX e-ink tablets with Google Play."),
             ("Which patterns work?", "PDF patterns with a chart drawn on a grid. It is tested on dozens of DROPS charts; the app finds the grid and rows itself, and you can correct the edges by hand."),
             ("What can I do without buying?", "Add projects, open patterns, browse the pages and mark charts. Knitting row by row with the highlighted row needs the free trial or a purchase."),
             ("I have a new phone. Do I pay again?", "No. Install Gabi Knits with the same Google account and tap “Restore purchases”."),
             ("How do I cancel the subscription?", "In Google Play: Payments & subscriptions → Subscriptions. Your projects stay where they are."),
             ("Is there an iPhone or iPad version?", "Not yet – Android comes first.")],
        contact_t="Contact", contact_p="Questions, ideas, a pattern that doesn’t work? Write to us:",
        vat="VAT ID PL7321956817", privacy="Privacy policy",
    ),
    "pl": dict(
        title="Gabi Knits – czytnik schematów dziewiarskich na Androida i e-ink BOOX",
        desc="Gabi Knits otwiera wzory PDF, sam znajduje schemat i prowadzi rząd po rzędzie. Na telefon, tablet i e-ink BOOX. Bez konta i bez reklam.",
        nav=("Jak to działa", "Co potrafi", "Cena", "Pytania", "Kontakt"),
        claim="Dziergaj ze schematu rząd po rzędzie.",
        intro="Gabi Knits otwiera wzory PDF, znajduje schemat na stronie i wyraźnie zaznacza rząd, który dziergasz. Postęp w każdym projekcie zapisuje się sam.",
        soon="Wkrótce w Google Play",
        devices="Telefony z Androidem · tablety · tablety e-ink BOOX",
        pledge="Bez konta · bez reklam · bez śledzenia",
        shots=("Tablet e-ink BOOX", "Telefon", "Tablet"),
        alt=("Gabi Knits na tablecie e-ink BOOX: schemat z obwiedzionym bieżącym rzędem", "Gabi Knits na telefonie: bieżący rząd podświetlony na żółto", "Gabi Knits na tablecie w poziomie: schemat i przyciski rzędu obok siebie"),
        how_t="Jak to działa", how_l="Trzy kroki od PDF-a do drutów.",
        steps=[("Otwórz wzór", "Dodaj wzór PDF jako projekt. Dostaje własną nazwę i pamięta, gdzie skończyłaś."),
               ("Dotknij schematu", "Gabi Knits sama znajduje ramkę i rzędy schematu. Krawędzie możesz w razie potrzeby poprawić."),
               ("Dziergaj rząd po rzędzie", "Bieżący rząd jest wyraźnie zaznaczony. Jeden duży przycisk prowadzi do następnego – wygodnie jedną ręką.")],
        feat_t="Co potrafi", feat_l="Tylko to, co pomaga skończyć rząd – nic, co by przeszkadzało.",
        feats=[("Kilka schematów w jednym wzorze", "Przód, tył i rękawy – każdy schemat pamięta swój rząd i historię."),
               ("Przełączanie jednym dotknięciem", "Pływająca lista albo pasek przy liczniku, który nie zasłania strony."),
               ("Legenda pod ręką", "Zaznacz objaśnienie symboli raz i otwieraj je nad stroną, nie gubiąc rzędu."),
               ("Rząd idzie za Tobą", "Schemat może przesuwać się pod stojącym paskiem – bieżący rząd zostaje na środku ekranu."),
               ("Licznik czasu", "Zobacz, ile trwał projekt – liczy tylko wtedy, gdy go włączysz."),
               ("Sześć języków", "Polski, angielski, niemiecki, norweski, duński i szwedzki.")],
        eink_badge="Stworzona<br>dla e-inku", eink_t="Spokojna na e-inku",
        eink_p="Gabi Knits powstała na BOOX Note Air. Na e-inku nie ma animacji ani kolorów niosących znaczenie – czerń na bieli, duże przyciski i duże numery rzędów, czytelne znad robótki. Na telefonie i zwykłym tablecie korzysta z koloru i płynnego ruchu.",
        price_t="Cena", price_l="Przez 14 dni wypróbujesz wszystko za darmo. Potem wybierz, co Ci pasuje.",
        plans=[("Miesięcznie", "6,99 zł", "za miesiąc", True), ("Rocznie", "14,99 zł", "za rok", True), ("Na zawsze", "39,99 zł", "jednorazowo", False)],
        best="Najkorzystniej", trial_yes="<b>14 dni za darmo</b>, potem odnawia się samo, jeśli nie anulujesz.", trial_no="Płacisz raz i masz na zawsze.",
        price_note="Jedna darmowa próba na konto Google. Subskrypcję anulujesz w każdej chwili w Google Play.",
        priv_t="Twoje wzory zostają u Ciebie",
        priv_points=("Bez konta", "Bez reklam", "Bez śledzenia i analityki", "Działa bez internetu"),
        priv_p="Wzory PDF, projekty i numery rzędów zostają na Twoim urządzeniu. Aplikacja łączy się z internetem tylko po to, żeby obsłużyć zakup i sprawdzić dostęp.",
        priv_link="Przeczytaj politykę prywatności",
        faq_t="Pytania",
        faq=[("Czy potrzebuję konta?", "Nie. Nie ma rejestracji ani logowania. Zakup idzie przez Twoje konto Google Play."),
             ("Czy działa bez internetu?", "Tak. Czytanie i dzierganie nigdy nie wymagają internetu. Połączenie jest potrzebne tylko do zakupu i co jakiś czas do potwierdzenia subskrypcji."),
             ("Na jakich urządzeniach działa?", "Android 8.1 lub nowszy: telefony, tablety i tablety e-ink BOOX ze Sklepem Play."),
             ("Jakie wzory się nadają?", "Wzory PDF ze schematem na siatce. Sprawdzona na kilkudziesięciu schematach DROPS; siatkę i rzędy znajduje sama, a krawędzie możesz poprawić ręcznie."),
             ("Co mogę bez zakupu?", "Dodawać projekty, otwierać wzory, przeglądać strony i zaznaczać schematy. Dzierganie rząd po rzędzie z podświetlonym rzędem wymaga darmowej próby albo zakupu."),
             ("Mam nowy telefon. Płacę jeszcze raz?", "Nie. Zainstaluj Gabi Knits na tym samym koncie Google i dotknij „Przywróć zakupy”."),
             ("Jak anulować subskrypcję?", "W Google Play: Płatności i subskrypcje → Subskrypcje. Projekty zostają na miejscu."),
             ("Czy jest wersja na iPhone’a albo iPada?", "Jeszcze nie – najpierw Android.")],
        contact_t="Kontakt", contact_p="Pytanie, pomysł, wzór, który nie działa? Napisz do nas:",
        vat="NIP 7321956817", privacy="Polityka prywatności",
    ),
    "de": dict(
        title="Gabi Knits – Strickdiagramm-Leser für Android und BOOX E-Ink",
        desc="Gabi Knits öffnet deine PDF-Strickanleitungen, findet das Diagramm und führt dich Reihe für Reihe. Für Android-Handys, Tablets und BOOX E-Ink. Kein Konto, keine Werbung.",
        nav=("So geht’s", "Funktionen", "Preis", "Fragen", "Kontakt"),
        claim="Stricke nach Diagramm, Reihe für Reihe.",
        intro="Gabi Knits öffnet deine PDF-Anleitungen, findet das Diagramm auf der Seite und markiert deutlich die Reihe, die du strickst. Der Fortschritt jedes Projekts wird automatisch gespeichert.",
        soon="Bald bei Google Play",
        devices="Android-Handys · Tablets · BOOX E-Ink-Tablets",
        pledge="Kein Konto · keine Werbung · kein Tracking",
        shots=("BOOX E-Ink-Tablet", "Handy", "Tablet"),
        alt=("Gabi Knits auf einem BOOX E-Ink-Tablet: Diagramm mit umrahmter aktueller Reihe", "Gabi Knits auf dem Handy: die aktuelle Reihe gelb hervorgehoben", "Gabi Knits auf einem Tablet im Querformat: Diagramm und Reihentasten nebeneinander"),
        how_t="So geht’s", how_l="In drei Schritten vom PDF zu den Nadeln.",
        steps=[("Öffne deine Anleitung", "Füge eine PDF-Anleitung als Projekt hinzu. Es bekommt einen eigenen Namen und merkt sich, wo du aufgehört hast."),
               ("Tippe auf das Diagramm", "Gabi Knits findet Rahmen und Reihen des Diagramms selbst. Die Ränder kannst du bei Bedarf korrigieren."),
               ("Stricke Reihe für Reihe", "Die aktuelle Reihe ist deutlich markiert. Eine große Taste bringt dich zur nächsten – bequem mit einer Hand.")],
        feat_t="Was sie kann", feat_l="Nur was dir hilft, die Reihe zu beenden – nichts, was stört.",
        feats=[("Mehrere Diagramme in einer Anleitung", "Vorderteil, Rückenteil, Ärmel – jedes Diagramm behält seine Reihe und seinen Verlauf."),
               ("Wechsel mit einem Tippen", "Eine schwebende Liste oder eine Leiste am Reihenzähler, die die Seite nie verdeckt."),
               ("Die Legende griffbereit", "Markiere die Zeichenerklärung einmal und öffne sie über der Seite, ohne die Reihe zu verlieren."),
               ("Die Reihe folgt dir", "Das Diagramm kann sich unter einer festen Leiste bewegen – die aktuelle Reihe bleibt in der Bildschirmmitte."),
               ("Strickzeit", "Sieh, wie lange ein Projekt gedauert hat – die Uhr läuft nur, wenn du sie startest."),
               ("Sechs Sprachen", "Deutsch, Englisch, Polnisch, Norwegisch, Dänisch und Schwedisch.")],
        eink_badge="Gemacht<br>für E-Ink", eink_t="Ruhig auf E-Ink",
        eink_p="Gabi Knits ist auf einem BOOX Note Air entstanden. Auf E-Ink gibt es keine Animationen und keine bedeutungstragenden Farben – Schwarz auf Weiß, große Tasten und große Reihennummern, lesbar über dem Strickzeug. Auf Handys und normalen Tablets nutzt sie Farbe und flüssige Bewegung.",
        price_t="Preis", price_l="Probiere 14 Tage lang alles kostenlos aus. Dann wähle, was zu dir passt.",
        plans=[("Monatlich", "2,99 €", "pro Monat", True), ("Jährlich", "5,99 €", "pro Jahr", True), ("Für immer", "14,99 €", "einmalig", False)],
        best="Am günstigsten", trial_yes="<b>14 Tage kostenlos</b>, danach automatische Verlängerung, wenn du nicht kündigst.", trial_no="Einmal zahlen, für immer behalten.",
        price_note="Ein kostenloser Test pro Google-Konto. Preise in Euro; Google Play zeigt den Preis in deiner Währung. Jederzeit in Google Play kündbar.",
        priv_t="Deine Anleitungen bleiben bei dir",
        priv_points=("Kein Konto", "Keine Werbung", "Kein Tracking, keine Analyse", "Funktioniert offline"),
        priv_p="Deine PDF-Anleitungen, Projekte und Reihennummern bleiben auf deinem Gerät. Die App nutzt das Internet nur, um einen Kauf abzuwickeln und deinen Zugang zu prüfen.",
        priv_link="Datenschutzerklärung lesen",
        faq_t="Fragen",
        faq=[("Brauche ich ein Konto?", "Nein. Keine Registrierung, keine Anmeldung. Käufe laufen über dein Google-Play-Konto."),
             ("Funktioniert sie ohne Internet?", "Ja. Lesen und Stricken brauchen nie Internet. Eine Verbindung ist nur zum Kaufen und ab und zu zur Bestätigung des Abos nötig."),
             ("Auf welchen Geräten läuft sie?", "Android 8.1 oder neuer: Handys, Tablets und BOOX E-Ink-Tablets mit Google Play."),
             ("Welche Anleitungen passen?", "PDF-Anleitungen mit einem Diagramm auf einem Raster. Getestet mit Dutzenden DROPS-Diagrammen; Raster und Reihen findet die App selbst, die Ränder kannst du von Hand korrigieren."),
             ("Was geht ohne Kauf?", "Projekte anlegen, Anleitungen öffnen, Seiten durchblättern und Diagramme markieren. Reihe für Reihe mit hervorgehobener Reihe stricken erfordert den kostenlosen Test oder einen Kauf."),
             ("Ich habe ein neues Handy. Zahle ich noch einmal?", "Nein. Installiere Gabi Knits mit demselben Google-Konto und tippe auf „Käufe wiederherstellen“."),
             ("Wie kündige ich das Abo?", "In Google Play: Zahlungen und Abos → Abos. Deine Projekte bleiben, wo sie sind."),
             ("Gibt es eine Version für iPhone oder iPad?", "Noch nicht – zuerst Android.")],
        contact_t="Kontakt", contact_p="Fragen, Ideen, eine Anleitung, die nicht funktioniert? Schreib uns:",
        vat="USt-IdNr. PL7321956817", privacy="Datenschutzerklärung",
    ),
    "nb": dict(
        title="Gabi Knits – leser for strikkediagrammer på Android og BOOX e-ink",
        desc="Gabi Knits åpner PDF-strikkeoppskriftene dine, finner diagrammet og leder deg rad for rad. For Android-telefoner, nettbrett og BOOX e-ink. Ingen konto, ingen reklame.",
        nav=("Slik virker det", "Funksjoner", "Pris", "Spørsmål", "Kontakt"),
        claim="Strikk etter diagram, rad for rad.",
        intro="Gabi Knits åpner PDF-oppskriftene dine, finner diagrammet på siden og markerer tydelig raden du strikker. Fremdriften i hvert prosjekt lagres automatisk.",
        soon="Kommer snart på Google Play",
        devices="Android-telefoner · nettbrett · BOOX e-ink-nettbrett",
        pledge="Ingen konto · ingen reklame · ingen sporing",
        shots=("BOOX e-ink-nettbrett", "Telefon", "Nettbrett"),
        alt=("Gabi Knits på et BOOX e-ink-nettbrett: diagram med gjeldende rad innrammet", "Gabi Knits på telefon: gjeldende rad uthevet i gult", "Gabi Knits på nettbrett i liggende format: diagram og radknapper side om side"),
        how_t="Slik virker det", how_l="Tre trinn fra PDF til pinnene.",
        steps=[("Åpne oppskriften", "Legg til en PDF-oppskrift som prosjekt. Det får sitt eget navn og husker hvor du stoppet."),
               ("Trykk på diagrammet", "Gabi Knits finner rammen og radene i diagrammet selv. Kantene kan du rette ved behov."),
               ("Strikk rad for rad", "Gjeldende rad er tydelig markert. Én stor knapp tar deg til neste rad – lett med én hånd.")],
        feat_t="Hva den kan", feat_l="Bare det som hjelper deg å fullføre raden – ingenting som er i veien.",
        feats=[("Flere diagrammer i én oppskrift", "Forstykke, bakstykke og ermer – hvert diagram husker sin rad og historikk."),
               ("Bytt med ett trykk", "En flytende liste eller en stripe ved radtelleren som aldri dekker siden."),
               ("Tegnforklaringen for hånden", "Marker tegnforklaringen én gang og åpne den over siden uten å miste raden."),
               ("Raden følger deg", "Diagrammet kan flytte seg under en fast stripe – gjeldende rad blir i midten av skjermen."),
               ("Strikketid", "Se hvor lang tid et prosjekt tok – klokken går bare når du starter den."),
               ("Seks språk", "Norsk, engelsk, polsk, tysk, dansk og svensk.")],
        eink_badge="Laget<br>for e-ink", eink_t="Rolig på e-ink",
        eink_p="Gabi Knits ble laget på en BOOX Note Air. På e-ink er det ingen animasjoner eller farger som bærer mening – svart på hvitt, store knapper og store radnumre du kan lese over strikketøyet. På telefoner og vanlige nettbrett bruker den farger og jevn bevegelse.",
        price_t="Pris", price_l="Prøv alt gratis i 14 dager. Velg så det som passer deg.",
        plans=[("Månedlig", "2,99 €", "per måned", True), ("Årlig", "5,99 €", "per år", True), ("For alltid", "14,99 €", "engangsbetaling", False)],
        best="Mest lønnsomt", trial_yes="<b>14 dager gratis</b>, fornyes deretter automatisk hvis du ikke sier opp.", trial_no="Betal én gang, behold den for alltid.",
        price_note="Én gratis prøveperiode per Google-konto. Prisene er i euro; Google Play viser prisen i din valuta. Si opp når som helst i Google Play.",
        priv_t="Oppskriftene dine blir hos deg",
        priv_points=("Ingen konto", "Ingen reklame", "Ingen sporing eller analyse", "Virker uten internett"),
        priv_p="PDF-oppskriftene, prosjektene og radnumrene dine blir på enheten din. Appen bruker internett bare til å gjennomføre et kjøp og sjekke at du har tilgang.",
        priv_link="Les personvernerklæringen",
        faq_t="Spørsmål",
        faq=[("Trenger jeg en konto?", "Nei. Ingen registrering og ingen innlogging. Kjøp går gjennom Google Play-kontoen din."),
             ("Virker den uten internett?", "Ja. Lesing og strikking trenger aldri internett. Du trenger tilkobling bare for å kjøpe og av og til for å bekrefte abonnementet."),
             ("Hvilke enheter virker den på?", "Android 8.1 eller nyere: telefoner, nettbrett og BOOX e-ink-nettbrett med Google Play."),
             ("Hvilke oppskrifter passer?", "PDF-oppskrifter med diagram på rutenett. Testet på dusinvis av DROPS-diagrammer; appen finner rutenettet og radene selv, og kantene kan du rette for hånd."),
             ("Hva kan jeg gjøre uten å kjøpe?", "Legge til prosjekter, åpne oppskrifter, bla i sidene og markere diagrammer. Å strikke rad for rad med uthevet rad krever gratis prøveperiode eller kjøp."),
             ("Jeg har ny telefon. Betaler jeg igjen?", "Nei. Installer Gabi Knits med samme Google-konto og trykk «Gjenopprett kjøp»."),
             ("Hvordan sier jeg opp abonnementet?", "I Google Play: Betalinger og abonnementer → Abonnementer. Prosjektene dine blir der de er."),
             ("Finnes det en versjon for iPhone eller iPad?", "Ikke ennå – Android kommer først.")],
        contact_t="Kontakt", contact_p="Spørsmål, ideer, en oppskrift som ikke virker? Skriv til oss:",
        vat="MVA-nr. PL7321956817", privacy="Personvernerklæring",
    ),
    "da": dict(
        title="Gabi Knits – læser til strikkediagrammer på Android og BOOX e-ink",
        desc="Gabi Knits åbner dine PDF-strikkeopskrifter, finder diagrammet og fører dig række for række. Til Android-telefoner, tablets og BOOX e-ink. Ingen konto, ingen reklamer.",
        nav=("Sådan virker det", "Funktioner", "Pris", "Spørgsmål", "Kontakt"),
        claim="Strik efter diagram, række for række.",
        intro="Gabi Knits åbner dine PDF-opskrifter, finder diagrammet på siden og markerer tydeligt den række, du strikker. Fremskridtet i hvert projekt gemmes automatisk.",
        soon="Kommer snart på Google Play",
        devices="Android-telefoner · tablets · BOOX e-ink-tablets",
        pledge="Ingen konto · ingen reklamer · ingen sporing",
        shots=("BOOX e-ink-tablet", "Telefon", "Tablet"),
        alt=("Gabi Knits på en BOOX e-ink-tablet: diagram med den aktuelle række indrammet", "Gabi Knits på telefon: den aktuelle række fremhævet med gult", "Gabi Knits på en tablet på langs: diagram og rækkeknapper side om side"),
        how_t="Sådan virker det", how_l="Tre trin fra PDF til pindene.",
        steps=[("Åbn din opskrift", "Tilføj en PDF-opskrift som projekt. Det får sit eget navn og husker, hvor du stoppede."),
               ("Tryk på diagrammet", "Gabi Knits finder selv diagrammets ramme og rækker. Kanterne kan du rette efter behov."),
               ("Strik række for række", "Den aktuelle række er tydeligt markeret. Én stor knap fører dig til næste række – nemt med én hånd.")],
        feat_t="Hvad den kan", feat_l="Kun det, der hjælper dig med at gøre rækken færdig – intet, der er i vejen.",
        feats=[("Flere diagrammer i én opskrift", "Forstykke, ryg og ærmer – hvert diagram husker sin række og historik."),
               ("Skift med ét tryk", "En flydende liste eller en bjælke ved rækketælleren, der aldrig dækker siden."),
               ("Symbolforklaringen ved hånden", "Markér symbolforklaringen én gang og åbn den over siden uden at miste rækken."),
               ("Rækken følger dig", "Diagrammet kan flytte sig under en fast bjælke – den aktuelle række bliver midt på skærmen."),
               ("Strikketid", "Se, hvor lang tid et projekt tog – uret går kun, når du starter det."),
               ("Seks sprog", "Dansk, engelsk, polsk, tysk, norsk og svensk.")],
        eink_badge="Lavet<br>til e-ink", eink_t="Rolig på e-ink",
        eink_p="Gabi Knits blev skabt på en BOOX Note Air. På e-ink er der ingen animationer eller farver, der bærer betydning – sort på hvidt, store knapper og store rækkenumre, du kan læse over strikketøjet. På telefoner og almindelige tablets bruger den farver og glidende bevægelse.",
        price_t="Pris", price_l="Prøv alt gratis i 14 dage. Vælg så det, der passer dig.",
        plans=[("Månedlig", "2,99 €", "pr. måned", True), ("Årlig", "5,99 €", "pr. år", True), ("For altid", "14,99 €", "engangsbetaling", False)],
        best="Bedst værdi", trial_yes="<b>14 dage gratis</b>, fornyes derefter automatisk, medmindre du opsiger.", trial_no="Betal én gang, behold den for altid.",
        price_note="Én gratis prøveperiode pr. Google-konto. Priserne er i euro; Google Play viser prisen i din valuta. Opsig når som helst i Google Play.",
        priv_t="Dine opskrifter bliver hos dig",
        priv_points=("Ingen konto", "Ingen reklamer", "Ingen sporing eller analyse", "Virker uden internet"),
        priv_p="Dine PDF-opskrifter, projekter og rækkenumre bliver på din enhed. Appen bruger kun internettet til at gennemføre et køb og kontrollere, at du har adgang.",
        priv_link="Læs privatlivspolitikken",
        faq_t="Spørgsmål",
        faq=[("Skal jeg have en konto?", "Nej. Ingen oprettelse og intet login. Køb går gennem din Google Play-konto."),
             ("Virker den uden internet?", "Ja. Læsning og strikning kræver aldrig internet. Forbindelse er kun nødvendig for at købe og en gang imellem for at bekræfte abonnementet."),
             ("Hvilke enheder virker den på?", "Android 8.1 eller nyere: telefoner, tablets og BOOX e-ink-tablets med Google Play."),
             ("Hvilke opskrifter passer?", "PDF-opskrifter med et diagram på et gitter. Testet på snesevis af DROPS-diagrammer; appen finder selv gitteret og rækkerne, og kanterne kan du rette i hånden."),
             ("Hvad kan jeg uden at købe?", "Tilføje projekter, åbne opskrifter, bladre i siderne og markere diagrammer. At strikke række for række med fremhævet række kræver den gratis prøveperiode eller et køb."),
             ("Jeg har en ny telefon. Betaler jeg igen?", "Nej. Installer Gabi Knits med samme Google-konto og tryk på »Gendan køb«."),
             ("Hvordan opsiger jeg abonnementet?", "I Google Play: Betalinger og abonnementer → Abonnementer. Dine projekter bliver, hvor de er."),
             ("Findes der en version til iPhone eller iPad?", "Ikke endnu – Android kommer først.")],
        contact_t="Kontakt", contact_p="Spørgsmål, idéer, en opskrift, der ikke virker? Skriv til os:",
        vat="Moms-nr. PL7321956817", privacy="Privatlivspolitik",
    ),
    "sv": dict(
        title="Gabi Knits – läsare för stickdiagram på Android och BOOX e-ink",
        desc="Gabi Knits öppnar dina stickmönster i PDF, hittar diagrammet och guidar dig varv för varv. För Android-telefoner, surfplattor och BOOX e-ink. Inget konto, ingen reklam.",
        nav=("Så fungerar det", "Funktioner", "Pris", "Frågor", "Kontakt"),
        claim="Sticka efter diagram, varv för varv.",
        intro="Gabi Knits öppnar dina PDF-mönster, hittar diagrammet på sidan och markerar tydligt varvet du stickar. Framstegen i varje projekt sparas automatiskt.",
        soon="Kommer snart till Google Play",
        devices="Android-telefoner · surfplattor · BOOX e-ink-plattor",
        pledge="Inget konto · ingen reklam · ingen spårning",
        shots=("BOOX e-ink-platta", "Telefon", "Surfplatta"),
        alt=("Gabi Knits på en BOOX e-ink-platta: diagram med det aktuella varvet inramat", "Gabi Knits på telefon: det aktuella varvet markerat i gult", "Gabi Knits på en surfplatta liggande: diagram och varvknappar sida vid sida"),
        how_t="Så fungerar det", how_l="Tre steg från PDF till stickorna.",
        steps=[("Öppna ditt mönster", "Lägg till ett PDF-mönster som projekt. Det får ett eget namn och minns var du slutade."),
               ("Tryck på diagrammet", "Gabi Knits hittar själv diagrammets ram och varv. Kanterna kan du justera vid behov."),
               ("Sticka varv för varv", "Det aktuella varvet är tydligt markerat. En stor knapp tar dig till nästa varv – enkelt med en hand.")],
        feat_t="Vad den kan", feat_l="Bara det som hjälper dig att sticka klart varvet – inget som är i vägen.",
        feats=[("Flera diagram i ett mönster", "Framstycke, bakstycke och ärmar – varje diagram minns sitt varv och sin historik."),
               ("Byt med ett tryck", "En flytande lista eller en list vid varvräknaren som aldrig täcker sidan."),
               ("Teckenförklaringen till hands", "Markera teckenförklaringen en gång och öppna den över sidan utan att tappa varvet."),
               ("Varvet följer dig", "Diagrammet kan flytta sig under en fast list – det aktuella varvet stannar mitt på skärmen."),
               ("Sticktid", "Se hur lång tid ett projekt tog – klockan går bara när du startar den."),
               ("Sex språk", "Svenska, engelska, polska, tyska, norska och danska.")],
        eink_badge="Gjord<br>för e-ink", eink_t="Lugn på e-ink",
        eink_p="Gabi Knits skapades på en BOOX Note Air. På e-ink finns inga animationer eller färger som bär betydelse – svart på vitt, stora knappar och stora varvnummer som syns ovanför stickningen. På telefoner och vanliga surfplattor använder den färg och mjuka rörelser.",
        price_t="Pris", price_l="Prova allt gratis i 14 dagar. Välj sedan det som passar dig.",
        plans=[("Månadsvis", "2,99 €", "per månad", True), ("Årsvis", "5,99 €", "per år", True), ("För alltid", "14,99 €", "engångsbetalning", False)],
        best="Mest prisvärd", trial_yes="<b>14 dagar gratis</b>, förnyas sedan automatiskt om du inte säger upp.", trial_no="Betala en gång, behåll den för alltid.",
        price_note="En gratis provperiod per Google-konto. Priserna är i euro; Google Play visar priset i din valuta. Säg upp när som helst i Google Play.",
        priv_t="Dina mönster stannar hos dig",
        priv_points=("Inget konto", "Ingen reklam", "Ingen spårning eller analys", "Fungerar utan internet"),
        priv_p="Dina PDF-mönster, projekt och varvnummer stannar på din enhet. Appen använder internet bara för att genomföra ett köp och kontrollera att du har åtkomst.",
        priv_link="Läs integritetspolicyn",
        faq_t="Frågor",
        faq=[("Behöver jag ett konto?", "Nej. Ingen registrering och ingen inloggning. Köp går via ditt Google Play-konto."),
             ("Fungerar den utan internet?", "Ja. Läsning och stickning kräver aldrig internet. Anslutning behövs bara för att köpa och ibland för att bekräfta prenumerationen."),
             ("Vilka enheter fungerar den på?", "Android 8.1 eller senare: telefoner, surfplattor och BOOX e-ink-plattor med Google Play."),
             ("Vilka mönster passar?", "PDF-mönster med ett diagram på ett rutnät. Testad på dussintals DROPS-diagram; appen hittar själv rutnätet och varven, och kanterna kan du justera för hand."),
             ("Vad kan jag göra utan att köpa?", "Lägga till projekt, öppna mönster, bläddra bland sidorna och markera diagram. Att sticka varv för varv med markerat varv kräver den gratis provperioden eller ett köp."),
             ("Jag har en ny telefon. Betalar jag igen?", "Nej. Installera Gabi Knits med samma Google-konto och tryck på ”Återställ köp”."),
             ("Hur säger jag upp prenumerationen?", "I Google Play: Betalningar och prenumerationer → Prenumerationer. Dina projekt stannar där de är."),
             ("Finns det en version för iPhone eller iPad?", "Inte än – Android kommer först.")],
        contact_t="Kontakt", contact_p="Frågor, idéer, ett mönster som inte fungerar? Skriv till oss:",
        vat="Momsreg.nr PL7321956817", privacy="Integritetspolicy",
    ),
}


def home(lang):
    return "" if lang == "en" else f"{lang}/"


def page(lang):
    t = T[lang]
    up = "" if lang == "en" else "../"          # do korzenia strony
    alts = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="https://gabiknits.app/{home(l)}">' for l in LANGS
    ) + '\n<link rel="alternate" hreflang="x-default" href="https://gabiknits.app/">'
    langs = lang_nav(lang, lambda l: f"{up}{home(l)}")
    ids = ("how", "features", "price", "faq", "contact")
    nav = "".join(f'<a href="#{i}">{escape(n)}</a>' for i, n in zip(ids, t["nav"]))
    steps = "".join(
        f'<div class="step"><div class="n">{k}</div><h3>{escape(a)}</h3><p>{escape(b)}</p></div>'
        for k, (a, b) in enumerate(t["steps"], 1)
    )
    feats = "".join(f"<li><strong>{escape(a)}</strong><span>{escape(b)}</span></li>" for a, b in t["feats"])
    plans = ""
    for k, (name, price, per, trial) in enumerate(t["plans"]):
        best = k == 1
        plans += (
            f'<div class="plan{" best" if best else ""}">'
            + (f'<span class="tag">{escape(t["best"])}</span>' if best else "")
            + f'<div class="name">{escape(name)}</div><div class="price">{escape(price)}</div>'
            + f'<div class="per">{escape(per)}</div>'
            + f'<div class="trial">{t["trial_yes"] if trial else escape(t["trial_no"])}</div></div>'
        )
    points = "".join(f"<li>{escape(p)}</li>" for p in t["priv_points"])
    faq = "".join(f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in t["faq"])
    privacy = f'{up}{"" if lang == "en" else lang + "/"}privacy/'
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(t["title"])}</title>
<meta name="description" content="{escape(t["desc"])}">
<link rel="icon" type="image/png" href="{up}favicon.png">
<link rel="stylesheet" href="{up}assets/site.css">
{alts}
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="{up}{home(lang)}"><img src="{up}assets/logo.png" alt="" width="40" height="40">Gabi Knits</a>
  <nav class="nav">{nav}</nav>
  {langs}
</div></header>
<main>
<section class="hero"><div class="wrap">
  <img class="logo" src="{up}assets/logo.png" width="400" height="416" alt="Gabi Knits">
  <h1>Gabi Knits</h1>
  <p class="claim">{escape(t["claim"])}</p>
  <p class="intro">{escape(t["intro"])}</p>
  <span class="soon">{escape(t["soon"])}</span>
  <p class="devices">{escape(t["devices"])}</p>
  <p class="pledge">{escape(t["pledge"])}</p>
</div></section>
<section class="shots"><div class="wrap">
  <div class="grid">
    <figure><div class="frame eink"><img src="{up}assets/shots/eink.svg" width="760" height="952" alt="" loading="lazy"></div><figcaption>{escape(t["shots"][0])}</figcaption></figure>
    <figure><div class="frame phone"><img src="{up}assets/shots/phone.svg" width="540" height="1071" alt="" loading="lazy"></div><figcaption>{escape(t["shots"][1])}</figcaption></figure>
  </div>
  <figure class="wide"><div class="frame tablet"><img src="{up}assets/shots/tablet.svg" width="1200" height="827" alt="" loading="lazy"></div><figcaption>{escape(t["shots"][2])}</figcaption></figure>
</div></section>
<section id="how"><div class="wrap">
  <h2>{escape(t["how_t"])}</h2><p class="lead">{escape(t["how_l"])}</p>
  <div class="steps">{steps}</div>
</div></section>
<section id="features" class="band"><div class="wrap">
  <h2>{escape(t["feat_t"])}</h2><p class="lead">{escape(t["feat_l"])}</p>
  <ul class="features">{feats}</ul>
</div></section>
<section><div class="wrap">
  <div class="eink-box"><div class="badge">{t["eink_badge"]}</div><div><h2>{escape(t["eink_t"])}</h2><p>{escape(t["eink_p"])}</p></div></div>
</div></section>
<section id="price" class="band"><div class="wrap">
  <h2>{escape(t["price_t"])}</h2><p class="lead">{escape(t["price_l"])}</p>
  <div class="plans">{plans}</div>
  <p class="note">{escape(t["price_note"])}</p>
</div></section>
<section><div class="wrap">
  <h2>{escape(t["priv_t"])}</h2>
  <ul class="privacy-points">{points}</ul>
  <p class="lead">{escape(t["priv_p"])}</p>
  <a href="{privacy}">{escape(t["priv_link"])} →</a>
</div></section>
<section id="faq" class="band faq"><div class="wrap">
  <h2>{escape(t["faq_t"])}</h2>
  {faq}
</div></section>
<section id="contact" class="contact"><div class="wrap">
  <h2>{escape(t["contact_t"])}</h2>
  <p>{escape(t["contact_p"])}</p>
  <a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>
</div></section>
</main>
<footer><div class="wrap">
  <span>Gabi Knits · {escape(COMPANY)} · {escape(t["vat"])}</span>
  <span><a href="{privacy}">{escape(t["privacy"])}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></span>
</div></footer>
</body>
</html>
"""


for lang in LANGS:
    out = ROOT / home(lang) / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(lang), encoding="utf-8")
    print("zapisano", out.relative_to(ROOT))

# Polityka prywatności jest pisana ręcznie - generator podmienia w niej tylko przełącznik języków.
for lang in LANGS:
    path = ROOT / home(lang) / "privacy" / "index.html"
    up = "../" if lang == "en" else "../../"
    text = path.read_text(encoding="utf-8")
    nav = lang_nav(lang, lambda l: f"{up}{home(l)}privacy/")
    text, n = re.subn(r'<nav class="lang"[^>]*>.*?</nav>', lambda _: nav, text, count=1, flags=re.S)
    assert n == 1, path
    path.write_text(text, encoding="utf-8")
    print("przełącznik języków:", path.relative_to(ROOT))
