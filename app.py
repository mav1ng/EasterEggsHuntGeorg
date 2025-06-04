import streamlit as st
from rapidfuzz import fuzz

# Set page config
st.set_page_config(page_title="Happy Belated Birthday Bro", layout="wide")

# Easter eggs (target answers) and their hints
EASTER_EGGS = [
    "Black Knight Halberd",
    "Isaac",
    "Global Elite",
    "Estus Flask",
    "Bloodborne",
    "Hollow Knight",
    "Nina Chuba",
    "Genta Miura",
    "Praise the Sun"
]

EASTER_EGG_HINTS = [
    "Look on the table.",
    "Take a closer look at the balls in this picture.",
    "Find yourself in perfect motion and look for details.",
    "You can drink it.",
    "Should be found in London.",
    "Always on your shoulder.",
    "Surprise on Halloween.",
    "Surprise guest in Nottingham",
    "Let's go to Konstanz."
]

def normalize_text(text):
    """Normalize text for more flexible matching"""
    if not text:
        return ""
    # Convert to lowercase and remove extra whitespace
    text = ' '.join(str(text).lower().split())
    # Remove common punctuation
    for char in ".,!?;:'\"()[]{}“”‘’":
        text = text.replace(char, '')
    return text

def check_answers(user_answers):
    """Check user answers against the target answers using fuzzy matching"""
    remaining_eggs = set(EASTER_EGGS)
    results = []
    
    # Pre-normalize all eggs for comparison
    normalized_eggs = {egg: normalize_text(egg) for egg in EASTER_EGGS}
    
    # First pass: Check for exact or fuzzy matches
    for user_answer in user_answers:
        normalized_answer = normalize_text(user_answer)
        
        if not normalized_answer:
            results.append((False, None))
            continue
            
        best_match = None
        best_score = 0
        
        for egg in list(remaining_eggs):  # Create a list to avoid modifying set during iteration
            # Try different matching strategies
            egg_norm = normalized_eggs[egg]
            
            # 1. Check for direct inclusion (either way)
            if normalized_answer in egg_norm or egg_norm in normalized_answer:
                score = 100
            else:
                # 2. Try different fuzzy matching strategies
                score1 = fuzz.ratio(normalized_answer, egg_norm)
                score2 = fuzz.partial_ratio(normalized_answer, egg_norm)
                score3 = fuzz.token_sort_ratio(normalized_answer, egg_norm)
                score4 = fuzz.token_set_ratio(normalized_answer, egg_norm)
                
                # Take the best score from all strategies
                score = max(score1, score2, score3, score4)
            
            # Be more lenient with shorter answers
            min_length = min(len(normalized_answer), len(egg_norm))
            if min_length <= 5 and score >= 70:  # Be more lenient with short answers
                score = max(score, 85)
                
            if score > best_score:
                best_score = score
                best_match = egg
        
        # Lower the threshold for matching
        if best_score >= 75:  # Reduced from 80 to 75 for more leniency
            remaining_eggs.discard(best_match)
            results.append((True, best_match))
        else:
            results.append((False, None))
    
    return results, remaining_eggs

def show_hint(remaining_eggs):
    """Show a hint for a remaining Easter egg"""
    if not remaining_eggs:
        st.info("All Easter eggs have been found!")
        return
    
    # Get the first remaining egg and its hint
    egg = next(iter(remaining_eggs))
    egg_index = EASTER_EGGS.index(egg)
    hint = EASTER_EGG_HINTS[egg_index]
    
    st.info(hint)
    
    # Rotate the remaining eggs so we show a different one next time
    remaining_list = list(remaining_eggs)
    rotated_remaining = set(remaining_list[1:] + [remaining_list[0]])
    return rotated_remaining

def main():
    # Initialize session state
    if 'remaining_eggs' not in st.session_state:
        st.session_state.remaining_eggs = set(EASTER_EGGS)
    
    # Title and subtitle
    st.title("Happy Belated Birthday Bro.")
    
    # Instruction text
    st.write("Enter the correct 9 Easter eggs from the photo collage page and submit to continue. "
             "You will get feedback when you submit and did not get everything right. In case you feel stuck press the"
             " hint button further down.")
    
    # Create text input fields
    user_answers = []
    for i in range(9):
        answer = st.text_input(f"Easter Egg {i+1}", key=f"egg_{i}")
        user_answers.append(answer if answer is not None else "")
    
    # Create buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        hint_clicked = st.button("Hint")
    with col2:
        submit_clicked = st.button("Submit")
    
    # Handle hint button
    if hint_clicked:
        st.session_state.remaining_eggs = show_hint(st.session_state.remaining_eggs)
    
    # Handle submit button
    if submit_clicked:
        # Check if all fields are filled
        if not all(user_answers):
            st.error("Please fill in all fields before submitting.")
            return
        
        # Check answers
        results, remaining_eggs = check_answers(user_answers)
        st.session_state.remaining_eggs = remaining_eggs
        all_correct = all(result[0] for result in results)
        
        # Display results
        if all_correct:
            st.balloons()
            st.success("🎉 Congratulations! You found all the Easter eggs! 🎉")
            
            # Emotional congratulation letter
            st.markdown("---")
            st.markdown("## 🎂 Happy Birthday, Bro! 🎉")
            st.markdown("""
            
            Wow, tatsächlich hast Du alle Easter-Eggs gefunden, und tatsächlich hätte
            ich auch absolut nichts anderes erwartet. Umso größer für Dich die Challenge –
            desto mehr Konzentration und Power hast Du, die Dinge anzugehen und zu bewältigen. 
            Das ist ja mal sowas von die krasseste Anime-Fähigkeit von der ich je gehört habe. Ja, und
            das ist definitiv eine Deiner vielen Qualitäten und Eigenschaften, die ich einfach lieb 
            gewonnen habe. 
            
            Mir ist beim Durchblättern der digitalen Fotobücher dieser eine Georg vor die Augen gekommen: 
            Über Jahre hinweg warst du da und hast mich in vielen Abenteuern – das erste mal Konstanz, 
            zusammen Fifa und Bier in Thomas Garten, die guten 1 1/2 Jahrzehnte Schulzeit inklusive Traumsturm
            (wir kennen uns ja tatsächlich schon mindestens zwei Jahrzehnte, brutal oder?), dann Zusammenziehen!! 
            und an 9 Jahren Zusammenwohnen haben wir gekratzt, minus London waren es wohl eher 8, 
            besucht hast du mich aber dort, erster Sonnenbrand des Jahres in Nottingham, und grundsätzlich 
            warst du irgendwie immer da. Immer da als der beste Freund, den man sich nur wünschen kann. Einfach immer. 
            
            Und bis auf Weiteres wirst Du immer die Person bleiben, mit der ich die meiste Zeit meines Lebens 
            verbringen durfte – bis auf meine Eltern vielleicht. Und es wird mindestens ein Jahrzehnt dauern 
            bis sich das ändern könnte. Und ich lächle einfach in mich hinein, weil das wird immer Teil von mir 
            sein und das wird nie jemand ändern können und ich bin einfach sehr sehr dankbar dafür. 
            
            Ich habe praktisch ein Fotoalbum mit Erinnerungen mit Dir und es hat unzählbar viele Seiten
            und keine von denen möchte ich wirklich aussortieren. Und wenn ich da so durchblättere, dann
            bin ich einfach zu Hause und fühle mich wie angekommen. 
            
            Mir ist aufgefallen, wieviele Hobbies und Interessen ich mit Dir immer geteilt habe und wie ähnlich
            sie noch immer sind. Die Runden Bierpong und Spikeball, in denen wir ins gleiche Team kommen und
            mit einem Schmunzeln abklatschen bevor es losgeht und das Gefühl, dass da in dem anderen Zimmer
            immer eine Person war, der ich alles erzählen kann, die mir zuhört, wenn ich von meinen Emotionen
            vollkommen überwältigt werde und auch da ist, wenn ich einfach nur bei Dir sein möchte und Dir 
            zuschaue mit rythmischem Parov Stellar wie du eines der schwierigsten Spiele der Welt speedrunst
            und ich mitfieber und das einfach so krass finde.
            Einfach diese krank tolle Zeit. 
            
            Für mich bedeutet das Schreiben hier so unglaublich viel, weil ich mir dabei wieder mit größtem
            Nachdruck vor Augen führe welche Abundance von Erinnerungen ich mit dir teile. Sei es wie Felix und 
            Du die Tequila-Flasche eigenhändig geleert habt in Konstanz, der Autokühler breakdown aufm Rückweg
            vom zweiten mal Konstanz, Schokoladenessen bei deinen Kindergeburtstagen, (wie hält eine Schokolade so
            viel kindischen Heißhunger und Ehrgeiz und vorallem Messer- und Gabelstiche aus?). Und stundelang am Stück auf
            einen Basketballkorb! kicken, bis der Abend anbricht, auf dem Arbeitslaptop von deinem Vater Need for Speed
            Hot Pursuit zocken mit Pfeiltasten und von dir neue Songs gezeigt bekommen, weil 
            Du deinen nächsten favourite mal wieder rauf und runter hörst bis Du ihn satt bist (und ich dann 
            anfange ihn laut aus meinem Zimmer zu spielen). Dein krassester No-Scope im Zurücklaufen
            ins Pit auf Long, Porridge und J und K League 5 Uhr morgens am Wochenende, wie du mich vom Instant-Kaffee
            zur French-Press bekehrt hast (danke), mir die coolsten Animes und Mangas gezeigt hast, wie wir in unserem 
            bürgerlichen Leben Tatort Sonntag abends geschaut haben, oft mit Soya Schnitzel von der Mühle,
            die lebhaften Runden Governor, mein erstes Festival, den ersten Monat zusammen 
            aufm Boden in der Ringstraße schlafen und bei Dunkelheit früh morgens mit Dein-Bus pendeln für 1.45€..
            Brudi ich könnte echt ewig weiterschreiben hier und das macht mich echt dieses nostalgische Happy-Sad-Happy.
            
            Du bist wirklich Du. Und das mit so einer Integrität, Intensität und Standfestigkeit und zu wissen, dass Du immer
            hinter einem stehst whatever happens hat ein Vertrauen geschaffen, das ich nie vergessen werde. Ich habe für Dich
            so viel Liebe übrig und ich freue mich unglaublich auf Deine Geburtstagsfeier auf der wir jetzt eventuell sind, 
            vermutlich liest Du das erst ein, zwei Tage, oder ein paar Tage später, weil die Gäste hätten ja warten
            müssen, aber vielleicht hast dus auch gerade auf der Feier gelöst. Who knows.. Ich bin mir sicher, dass die
            Feier sowas von genial ist und danach freue ich mich auf unsere Zeit in Schweden. 
            
            Im Italienischen würde ich jetzt sagen tvb. Das ist kurz für ti voglio bene. Und Giulia meint das heißt
            sowas wie 'I love you, bro'. 
            
            Viktor
            
            """, unsafe_allow_html=True)
        else:
            st.error("Some answers need correction. Here's your feedback:")
            for i, (is_correct, target) in enumerate(results):
                if is_correct:
                    st.success(f"✅ Easter Egg {i+1}: Correct!")
                else:
                    st.error(f"❌ Easter Egg {i+1}: Not quite right. Try again!")
            
            st.warning("💡 Hint: Make sure you're using the correct spelling and check for any typos.")

if __name__ == "__main__":
    main()
