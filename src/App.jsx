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
  const [mode, setMode] = useState("words");

  const [index, setIndex] = useState(0);
  const [show, setShow] = useState(false);

  const [selectedArticle, setSelectedArticle] = useState("all");

  useEffect(() => {
    fetch("/words.json")
      .then((res) => res.json())
      .then((data) => setWords(shuffleArray(data)));

    fetch("/verbs.json")
      .then((res) => res.json())
      .then((data) => setVerbs(shuffleArray(data)));
  }, []);

  const filteredWords = words.filter((word) => {
    return selectedArticle === "all" || word.article === selectedArticle;
  });

  const currentList =
    mode === "words" ? filteredWords : verbs;

  if (currentList.length === 0) {
    return <div style={styles.loading}>Загрузка...</div>;
  }

  const item = currentList[index];

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
  }

  return (
    <div style={styles.page}>
      <div style={styles.header}>
        <h1 style={styles.title}>Deutsch Trainer</h1>

        <p style={styles.counter}>
          {index + 1} / {currentList.length}
        </p>
      </div>

<div style={styles.content}>
      <div style={styles.modeButtons}>
        <button
          style={
            mode === "words"
              ? styles.activeModeButton
              : styles.modeButton
          }
          onClick={() => changeMode("words")}
        >
          Слова
        </button>

        <button
          style={
            mode === "verbs"
              ? styles.activeModeButton
              : styles.modeButton
          }
          onClick={() => changeMode("verbs")}
        >
          Глаголы
        </button>
      </div>

      {mode === "words" && (
        <div style={styles.articleButtons}>
          {["all", "der", "die", "das"].map((article) => (
            <button
              key={article}
              style={
                selectedArticle === article
                  ? styles.activeArticleButton
                  : styles.articleButton
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

      <div style={styles.progressOuter}>
        <div
          style={{
            ...styles.progressInner,
            width: `${((index + 1) / currentList.length) * 100}%`,
          }}
        />
      </div>

      <div
        style={styles.card}
        onClick={() => setShow(!show)}
      >
        {!show ? (
          <>
        

            <div style={styles.mainWord}>
              {mode === "words" ? item.de : item.infinitive || item.de}
            </div>

          </>
        ) : mode === "words" ? (
          <>
           

            <div style={styles.mainWord}>
              {item.ru}
            </div>

            <div style={styles.infoBox}>
              <div>
                <p style={styles.smallLabel}>
                  Артикль
                </p>

                <p style={styles.infoText}>
                  {item.article}
                </p>
              </div>

              <div>
                <p style={styles.smallLabel}>
                  Мн. число
                </p>

                <p style={styles.infoText}>
                  {item.plural}
                </p>
              </div>
            </div>
          </>
        ) : (
          <>
        

            <div style={styles.mainWord}>
              {item.ru}
            </div>

            <div style={styles.verbBox}>
              {Object.entries(item.conjugation).map(
                ([person, form]) => (
                  <div
                    key={person}
                    style={styles.verbRow}
                  >
                    <span style={styles.person}>
                      {person}
                    </span>

                    <span style={styles.form}>
                      {form}
                    </span>
                  </div>
                )
              )}
            </div>

            <div style={styles.exampleBox}>
              <p style={styles.exampleDe}>
                {item.example_de}
              </p>

              <p style={styles.exampleRu}>
                {item.example_ru}
              </p>
            </div>
          </>
        )}
      </div>

      <div style={styles.buttons}>
        <button
          style={styles.secondaryButton}
          onClick={prev}
        >
          Назад
        </button>

        <button
          style={styles.mainButton}
          onClick={() => setShow(!show)}
        >
          Перевернуть
        </button>

        <button
          style={styles.secondaryButton}
          onClick={next}
        >
          Дальше
        </button>
      </div>
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "#8888ab",
    color: "white",
    fontFamily: "Arial, sans-serif",
    padding: "16px",
    boxSizing: "border-box",
    
    display: "flex",
    flexDirection: "column",      
  },

  content: {
  flex: 1,
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
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
    maxWidth: 700,
    margin: "0 auto 16px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },

  title: {
    fontSize: "clamp(24px, 5vw, 52px)",
    margin: 0,
  },

  counter: {
    fontSize: 18,
    color: "#cbd5e1",
    margin: 0,
  },

  modeButtons: {
    maxWidth: 700,
    margin: "0 auto 16px",
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 10,
  },

  modeButton: {
    padding: "12px 16px",
    borderRadius: 18,
    border: "1px solid #cbd5e1",
    background: "white",
    color: "#111",
    fontSize: 18,
    fontWeight: 700,
    cursor: "pointer",
  },

  activeModeButton: {
    padding: "12px 16px",
    borderRadius: 18,
    border: "1px solid #38bdf8",
    background: "#38bdf8",
    color: "#0f172a",
    fontSize: 18,
    fontWeight: 700,
    cursor: "pointer",
  },

  articleButtons: {
    maxWidth: 700,
    margin: "0 auto 24px",
    display: "flex",
    gap: 10,
    flexWrap: "wrap",
    justifyContent: "center",
  },

  articleButton: {
    padding: "10px 16px",
    borderRadius: 999,
    border: "1px solid #cbd5e1",
    background: "white",
    color: "#111",
    fontSize: 16,
    cursor: "pointer",
  },

  activeArticleButton: {
    padding: "10px 16px",
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
  minHeight: 360,
  margin: "0 auto",
  background: "#78aee1",
  borderRadius: 28,
  boxShadow: "0 20px 60px rgba(0,0,0,0.35)",
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
  textAlign: "center",
  padding: 20,
  cursor: "pointer",
  boxSizing: "border-box",
},


mainWord: {
  fontSize: "clamp(32px, 6vw, 44px)",
  fontWeight: 800,
  lineHeight: 1.1,
  color: "white",
},

hint: {
  marginTop: 14,
  fontSize: 20,
  color: "#4b515a",
},

infoBox: {
  marginTop: 40,
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
  fontSize: 30,
  fontWeight: 700,
  margin: 0,
  color: "white",
},

verbBox: {
  marginTop: 26,
  width: "100%",
  maxWidth: 420,
  display: "grid",
  gap: 8,
},

verbRow: {
  display: "flex",
  justifyContent: "space-between",
  background: "rgba(255,255,255,0.35)",
  borderRadius: 14,
  padding: "8px 14px",
  fontSize: 20,
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
  marginTop: 24,
  background: "rgba(255,255,255,0.35)",
  borderRadius: 18,
  padding: 16,
  width: "100%",
  maxWidth: 520,
},

exampleDe: {
  fontSize: 22,
  fontWeight: 800,
  margin: "0 0 8px",
  color: "#0f172a",
},

exampleRu: {
  fontSize: 18,
  margin: 0,
  color: "#1f2937",
},

buttons: {
  maxWidth: 700,
  margin: "24px auto 0",
  display: "flex",
  flexWrap: "wrap",
  gap: 12,
},

mainButton: {
  flex: 1,
  minWidth: 120,
  padding: "14px 14px",
  borderRadius: 18,
  border: "none",
  background: "#38bdf8",
  color: "#0f172a",
  fontSize: 20,
  fontWeight: 700,
  cursor: "pointer",
},

secondaryButton: {
  flex: 1,
  minWidth: 120,
  padding: "10px 10px",
  borderRadius: 18,
  border: "1px solid #475569",
  background: "#1e293b",
  color: "white",
  fontSize: 20,
  fontWeight: 700,
  cursor: "pointer",
},
}