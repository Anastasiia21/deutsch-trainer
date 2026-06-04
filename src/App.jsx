import { useState, useEffect } from "react";

function shuffleArray(array) {
  const arr = [...array];

  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }

  return arr;
}

export default function App() {
  const [words, setWords] = useState([]);
  const [verbs, setVerbs] = useState([]);
  const [phrases, setPhrases] = useState([]);
  const [mode, setMode] = useState("words");
  

  const [index, setIndex] = useState(0);
  const [show, setShow] = useState(false);

  const [selectedArticle, setSelectedArticle] = useState("all");
  const [selectedLevel, setSelectedLevel] = useState("all");

  useEffect(() => {
    fetch("/words.json")
      .then((res) => res.json())
      .then((data) => setWords(shuffleArray(data)));

    fetch("/verbs.json")
      .then((res) => res.json())
      .then((data) => setVerbs(shuffleArray(data)));

    fetch("/phrases.json")
      .then((res) => res.json())
      .then((data) => setPhrases(shuffleArray(data))); 
  }, []);

  const filteredWords = words.filter((word) => {
    return selectedArticle === "all" || word.article === selectedArticle;
  });

  const filteredVerbs = verbs.filter((verb) => {
  return selectedLevel === "all" || verb.level === selectedLevel;
  });


  const currentList =
  mode === "words"
    ? filteredWords
    : mode === "verbs"
    ? filteredVerbs
    : phrases;

  if (currentList.length === 0) {
    return <div style={styles.loading}>Загрузка...</div>;
  }

  const item = currentList[index];
  const isPhone = typeof window !== "undefined" && window.innerWidth <= 480;

  function next() {
    setShow(false);
    setIndex((prev) => (prev + 1) % currentList.length);
  }

  function prev() {
    setShow(false);
    setIndex((prev) => (prev - 1 + currentList.length) % currentList.length);
  }

  function changeMode(newMode) {
  setMode(newMode);
  setIndex(0);
  setShow(false);

  if (newMode === "words") {
    setSelectedLevel("all");
  }

  if (newMode === "verbs") {
    setSelectedArticle("all");
  }
 }

  return (
    <div style={{ ...styles.page, ...(isPhone ? styles.phonePage : {}) }}>
      <div style={{ ...styles.header, ...(isPhone ? styles.phoneHeader : {}) }}>
        <h1 style={{ ...styles.title, ...(isPhone ? styles.phoneTitle : {}) }}>Deutsch Trainer</h1>

        <p style={{ ...styles.counter, ...(isPhone ? styles.phoneCounter : {}) }}>
          {index + 1} / {currentList.length}
        </p>
      </div>

<div style={styles.content}>
      <div style={{ ...styles.modeButtons, ...(isPhone ? styles.phoneModeButtons : {}) }}>
        <button
          style={
            mode === "words"
              ? { ...styles.activeModeButton, ...(isPhone ? styles.phoneModeButton : {}) }
              : { ...styles.modeButton, ...(isPhone ? styles.phoneModeButton : {}) }
          }
          onClick={() => changeMode("words")}
        >
          Слова
        </button>

        <button
          style={
            mode === "verbs"
              ? { ...styles.activeModeButton, ...(isPhone ? styles.phoneModeButton : {}) }
              : { ...styles.modeButton, ...(isPhone ? styles.phoneModeButton : {}) }
          }
          onClick={() => changeMode("verbs")}
        >
          Глаголы
        </button>
    

        <button
         style={
          mode === "phrases"
           ? { ...styles.activeModeButton, ...(isPhone ? styles.phoneModeButton : {}) }
           : { ...styles.modeButton, ...(isPhone ? styles.phoneModeButton : {}) }
          }
          onClick={() => changeMode("phrases")}
        >
         Фразы
        </button>
          </div>

      {mode === "words" && (
        <div style={{ ...styles.articleButtons, ...(isPhone ? styles.phoneArticleButtons : {}) }}>
          {["all", "der", "die", "das"].map((article) => (
            <button
              key={article}
              style={
                selectedArticle === article
                  ? { ...styles.activeArticleButton, ...(isPhone ? styles.phoneFilterButton : {}) }
                  : { ...styles.articleButton, ...(isPhone ? styles.phoneFilterButton : {}) }
              }
              onClick={() => {
                setSelectedArticle(article);
                setIndex(0);
                setShow(false);
              }}
            >
              {article === "all" ? "Все" : article}
            </button>
          ))}
        </div>
      )}

      {mode === "verbs" && (
  <div style={{ ...styles.levelButtons, ...(isPhone ? styles.phoneLevelButtons : {}) }}>
    {["all", "A1", "A2", "B1", "B2", "C1"].map((level) => (
      <button
        key={level}
        style={
          selectedLevel === level
            ? { ...styles.activeLevelButton, ...(isPhone ? styles.phoneFilterButton : {}) }
            : { ...styles.levelButton, ...(isPhone ? styles.phoneFilterButton : {}) }
        }
        onClick={() => {
          setSelectedLevel(level);
          setIndex(0);
          setShow(false);
        }}
      >
        {level === "all" ? "Все" : level}
      </button>
    ))}
  </div>
)}

      <div style={styles.progressOuter}>
        <div
          style={{
            ...styles.progressInner,
            width: `${((index + 1) / currentList.length) * 100}%`,
          }}
        />
      </div>

      
        <div
          style={{
            ...styles.card,
            ...(isPhone ? styles.phoneCard : {}),
            ...(!show ? styles.frontCard : styles.backCard),
            ...(isPhone && !show ? styles.phoneFrontCard : {}),
            ...(isPhone && show ? styles.phoneBackCard : {}),
          }}
          onClick={() => setShow(!show)}
        >
          {!show ? (
           <>
  <div style={{ ...styles.mainWord, ...styles.frontMainWord, ...(isPhone ? styles.phoneFrontMainWord : {}) }}>
    {mode === "words"
      ? item.de
      : mode === "verbs"
      ? item.infinitive || item.de
      : item.ru}
  </div>

  {mode === "verbs" && item.cases && (
    <div style={{ ...styles.frontCaseBox, ...(isPhone ? styles.phoneFrontCaseBox : {}) }}>
      Падеж: {Array.isArray(item.cases) ? item.cases.join(", ") : item.cases}
    </div>
  )}
</>
          ) : mode === "words" ? (
            <>
              <div style={{ ...styles.mainWord, ...(isPhone ? styles.phoneMainWord : {}) }}>{item.ru}</div>

              <div style={{ ...styles.infoBox, ...(isPhone ? styles.phoneInfoBox : {}) }}>
                <div>
                  <p style={styles.smallLabel}>Артикль</p>
                  <p style={styles.infoText}>{item.article}</p>
                </div>

                <div>
                  <p style={styles.smallLabel}>Мн. число</p>
                  <p style={styles.infoText}>{item.plural}</p>
                </div>
              </div>
            </>
          ) : mode === "verbs" ? (
            <>
              <div style={{ ...styles.mainWord, ...(isPhone ? styles.phoneMainWord : {}) }}>{item.ru}</div>

              <div style={{ ...styles.verbBox, ...(isPhone ? styles.phoneVerbBox : {}) }}>
                {Object.entries(item.conjugation).map(([person, form]) => (
                  <div key={person} style={{ ...styles.verbRow, ...(isPhone ? styles.phoneVerbRow : {}) }}>
                    <span style={styles.person}>{person}</span>
                    <span style={styles.form}>{form}</span>
                  </div>
                ))}
              </div>

              <div style={{ ...styles.exampleBox, ...(isPhone ? styles.phoneExampleBox : {}) }}>
                <p style={{ ...styles.exampleDe, ...(isPhone ? styles.phoneExampleDe : {}) }}>{item.example_de}</p>
                <p style={{ ...styles.exampleRu, ...(isPhone ? styles.phoneExampleRu : {}) }}>{item.example_ru}</p>
              </div>
            </>
          ) : (
            <>
              <div style={{ ...styles.mainWord, ...(isPhone ? styles.phoneMainWord : {}) }}>{item.de}</div>

              <div style={{ ...styles.exampleBox, ...(isPhone ? styles.phoneExampleBox : {}) }}>
                <p style={{ ...styles.exampleDe, ...(isPhone ? styles.phoneExampleDe : {}) }}>{item.example_de}</p>
                <p style={{ ...styles.exampleRu, ...(isPhone ? styles.phoneExampleRu : {}) }}>{item.example_ru}</p>
              </div>
            </>
          )}
        </div>

        <div style={{ ...styles.buttons, ...(isPhone ? styles.phoneButtons : {}) }}>
          <button style={{ ...styles.secondaryButton, ...(isPhone ? styles.phoneNavButton : {}) }} onClick={prev}>
            Назад
          </button>

          <button style={{ ...styles.mainButton, ...(isPhone ? styles.phoneNavButton : {}) }} onClick={() => setShow(!show)}>
            Перевернуть
          </button>

          <button style={{ ...styles.secondaryButton, ...(isPhone ? styles.phoneNavButton : {}) }} onClick={next}>
            Дальше
          </button>
        </div>
      </div>
    </div>
  );
}


const styles = {
  page: {
  minHeight: "100svh",
  background: "#8888ab",
  color: "white",
  fontFamily: "Arial, sans-serif",
  padding: "14px 14px 14px",
  boxSizing: "border-box",
  display: "flex",
  flexDirection: "column",
  overflowY: "auto",
},

content: {
  flex: 1,
  display: "flex",
  flexDirection: "column",
  justifyContent: "flex-start",
},

  loading: {
    minHeight: "100vh",
    background: "#f5f5f7",
    color: "#111",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: 32,
    fontFamily: "Arial, sans-serif",
  },

  header: {
  width: "100%",
  maxWidth: 700,
  margin: "0 auto 12px",
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
},

  title: {
    fontSize: "clamp(24px, 4.5vw, 46px)",
    margin: 0,
  },

  counter: {
    fontSize: 16,
    color: "#cbd5e1",
    margin: 0,
  },

  modeButtons: {
  width: "100%",
  maxWidth: 700,
  margin: "14px auto 18px",
  display: "grid",
  gridTemplateColumns: "1fr 1fr 1fr",
  gap: 10,
},

modeButton: {
   padding: "14px 16px",
  borderRadius: 18,
  border: "1px solid #cbd5e1",
  background: "white",
  color: "#111",
  fontSize: "clamp(18px, 3vw, 22px)",
  fontWeight: 700,
  cursor: "pointer",
  whiteSpace: "nowrap",
},

activeModeButton: {
  padding: "14px 16px",
  borderRadius: 18,
  border: "1px solid #38bdf8",
  background: "#38bdf8",
  color: "#0f172a",
  fontSize: "clamp(18px, 3vw, 22px)",
  fontWeight: 700,
  cursor: "pointer",
  whiteSpace: "nowrap",
},

articleButtons: {
  width: "100%",
  maxWidth: 700,
  margin: "0 auto 18px",
  display: "flex",
  gap: 10,
  flexWrap: "wrap",
  justifyContent: "center",
},

articleButton: {
  padding: "10px 18px",
  borderRadius: 999,
  border: "1px solid #cbd5e1",
  background: "white",
  color: "#111",
  fontSize: 16,
  fontWeight: 500,
  cursor: "pointer",
},

activeArticleButton: {
  padding: "10px 18px",
  borderRadius: 999,
  border: "1px solid #38bdf8",
  background: "#38bdf8",
  color: "#0f172a",
  fontSize: 16,
  fontWeight: 700,
  cursor: "pointer",
},

  card: {
  width: "100%",
  maxWidth: 700,
  margin: "0 auto",
  background: "#78aee1",
  borderRadius: 28,
  boxShadow: "0 20px 60px rgba(0,0,0,0.35)",
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
  textAlign: "center",
  cursor: "pointer",
  boxSizing: "border-box",
},

frontCard: {
  minHeight: "clamp(200px, 27svh, 260px)",
  padding: "28px 20px",
},

backCard: {
  minHeight: "auto",
  padding: 14,
},

mainWord: {
  fontSize: "clamp(26px, 5vw, 36px)",
  fontWeight: 800,
  lineHeight: 1.1,
  color: "white",
},

frontMainWord: {
  fontSize: "clamp(34px, 5.6vw, 46px)",
  letterSpacing: "0.01em",
},

hint: {
  marginTop: 14,
  fontSize: 17,
  color: "#4b515a",
},

infoBox: {
  marginTop: 28,
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: 20,
  width: "100%",
},

smallLabel: {
  color: "#2e343d",
  fontSize: 16,
  marginBottom: 8,
},

infoText: {
  fontSize: 24,
  fontWeight: 700,
  margin: 0,
  color: "white",
},

verbBox: {
  marginTop: 18,
  width: "100%",
  maxWidth: 420,
  display: "grid",
  gap: 6,
},

verbRow: {
  display: "flex",
  justifyContent: "space-between",
  background: "rgba(255,255,255,0.35)",
  borderRadius: 14,
  padding: "7px 14px",
  fontSize: 17,
},

person: {
  fontWeight: 700,
  color: "#1f2937",
},

form: {
  fontWeight: 800,
  color: "#0f172a",
},

exampleBox: {
  marginTop: 18,
  background: "rgba(255,255,255,0.35)",
  borderRadius: 18,
  padding: 14,
  width: "100%",
  maxWidth: 520,
},

exampleDe: {
  fontSize: 16,
  fontWeight: 800,
  margin: "0 0 8px",
  color: "#0f172a",
},

exampleRu: {
  fontSize: 16,
  margin: 0,
  color: "#1f2937",
},

buttons: {
  width: "100%",
  maxWidth: 700,
  margin: "16px auto 0",
  display: "grid",
  gridTemplateColumns: "1fr 1.35fr 1fr",
  gap: 10,
},

mainButton: {
  padding: "13px 8px",
  borderRadius: 18,
  border: "none",
  background: "#38bdf8",
  color: "#0f172a",
  fontSize: "clamp(14px, 3.5vw, 20px)",
  fontWeight: 700,
  cursor: "pointer",
  whiteSpace: "nowrap",
},

secondaryButton: {
  padding: "13px 8px",
  borderRadius: 18,
  border: "1px solid #475569",
  background: "#1e293b",
  color: "white",
  fontSize: "clamp(14px, 3.5vw, 20px)",
  fontWeight: 700,
  cursor: "pointer",
  whiteSpace: "nowrap",
},

caseBox: {
  marginTop: 18,
  padding: "10px 16px",
  borderRadius: 999,
  background: "rgba(255,255,255,0.35)",
  color: "#0f172a",
  fontSize: 16,
  fontWeight: 700,
},

frontCaseBox: {
  marginTop: 28,
  padding: "12px 22px",
  borderRadius: 999,
  background: "rgba(255,255,255,0.35)",
  color: "#0f172a",
  fontSize: "clamp(16px, 2.8vw, 19px)",
  fontWeight: 800,
},

levelButtons: {
  maxWidth: 700,
  margin: "0 auto 16px",
  display: "flex",
  gap: 10,
  flexWrap: "wrap",
  justifyContent: "center",
},

levelButton: {
  padding: "10px 16px",
  borderRadius: 999,
  border: "1px solid #cbd5e1",
  background: "white",
  color: "#111",
  fontSize: 16,
  cursor: "pointer",
},

activeLevelButton: {
  padding: "10px 16px",
  borderRadius: 999,
  border: "1px solid #38bdf8",
  background: "#38bdf8",
  color: "#0f172a",
  fontSize: 16,
  fontWeight: 700,
  cursor: "pointer",
},

phonePage: {
  minHeight: "100dvh",
  padding: "8px 8px 10px",
  overflowY: "hidden",
},

phoneHeader: {
  margin: "0 auto 8px",
},

phoneTitle: {
  fontSize: 22,
  lineHeight: 1.1,
},

phoneCounter: {
  fontSize: 15,
},

phoneModeButtons: {
  margin: "8px auto 10px",
  gap: 8,
},

phoneModeButton: {
  padding: "11px 8px",
  borderRadius: 16,
  fontSize: 22,
},

phoneArticleButtons: {
  margin: "0 auto 8px",
  gap: 6,
},

phoneLevelButtons: {
  margin: "0 auto 8px",
  gap: 6,
  flexWrap: "nowrap",
},

phoneFilterButton: {
  padding: "7px 13px",
  fontSize: 20,
},

phoneCard: {
  maxWidth: "100%",
  borderRadius: 24,
},

phoneFrontCard: {
  minHeight: "clamp(160px, 24dvh, 210px)",
  padding: "22px 14px",
},

phoneBackCard: {
  padding: 10,
},

phoneMainWord: {
  fontSize: 27,
},

phoneFrontMainWord: {
  fontSize: "clamp(30px, 8vw, 38px)",
},

phoneFrontCaseBox: {
  marginTop: 18,
  padding: "9px 16px",
  fontSize: 16,
},

phoneInfoBox: {
  marginTop: 16,
  gap: 12,
},

phoneVerbBox: {
  marginTop: 10,
  maxWidth: "100%",
  gap: 5,
},

phoneVerbRow: {
  padding: "6px 14px",
  fontSize: 16,
  borderRadius: 12,
},

phoneExampleBox: {
  marginTop: 10,
  padding: 10,
  borderRadius: 16,
},

phoneExampleDe: {
  fontSize: 16,
  margin: "0 0 6px",
},

phoneExampleRu: {
  fontSize: 15,
},

phoneButtons: {
  margin: "10px auto 0",
  gap: 8,
},

phoneNavButton: {
  padding: "11px 6px",
  borderRadius: 16,
  fontSize: 16,
},
};