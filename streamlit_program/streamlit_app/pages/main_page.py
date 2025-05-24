import streamlit as st

st.title("Vektorpakolási Segédprogram")

st.markdown("""

Ez az alkalmazás egy **segédprogram** a többdimenziós vektorpakolási algoritmusok teszteléséhez és elemzéséhez.

A fő funkciók:

- 🔄 **Algoritmusok futtatása egy fájlon**  
  Egy feltöltött bemeneti fájlon lefuttathatók az implementált algoritmusok, az eredmények (ládaszám) azonnal megjelennek.

- 🧾 ** Tesztpéldány Generátor**  
  Egyedi eloszlású és méretű tesztpéldák generálása különböző dimenziószámokra.

- 📉 **Alsó korlát számítása**  
  Egy adott fájl/fájlok alapján kiszámítható az elméleti minimális ládaszám.

""")