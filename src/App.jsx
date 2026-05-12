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
  const [index, setIndex] = useState(0);
  const [show, setShow] = useState(false);
  const [selectedArticle, setSelectedArticle] = useState("all");

  useEffect(() => {
    fetch("/words.json")
      .then((res) => res.json())
      .then((data) => setWords(shuffleArray(data)));
  }, []);

  if (words.length === 0) {
    return <div style={styles.loading}>Загрузка...</div>;
  }

  const filteredWords = words.filter((word) => {
    return selectedArticle === "all" || word.article === selectedArticle;
  });

  if (filteredWords.length === 0) {
    return (
      <div style={styles.page}>
        <h1 style={styles.title}>Deutsch Trainer</h1>

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

        <p style={{ textAlign: "center", fontSize: 24 }}>
          Нет слов с таким артиклем.
        </p>
      </div>
    );
  }

  const word = filteredWords[index];

  function next() {
    setShow(false);
    setIndex((prev) => (prev + 1) % filteredWords.length);
  }

  function prev() {
    setShow(false);
    setIndex((prev) => (prev - 1 + filteredWords.length) % filteredWords.length);
  }

  return (
    <div style={styles.page}>
      <div style={styles.header}>
        <h1 style={styles.title}>Deutsch Trainer</h1>
        <p style={styles.counter}>
          {index + 1} / {filteredWords.length}
        </p>
      </div>

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

      <div style={styles.progressOuter}>
        <div
          style={{
            ...styles.progressInner,
            width: `${((index + 1) / filteredWords.length) * 100}%`,
          }}
        />
      </div>

      <div style={styles.card} onClick={() => setShow(!show)}>
        {!show ? (
          <>
            <p style={styles.label}>Немецкий</p>
            <div style={styles.mainWord}>{word.de}</div>
            <p style={styles.hint}>Нажми, чтобы увидеть перевод</p>
          </>
        ) : (
          <>
            <p style={styles.label}>Русский</p>
            <div style={styles.mainWord}>{word.ru}</div>

            <div style={styles.infoBox}>
              <div>
                <p style={styles.smallLabel}>Артикль</p>
                <p style={styles.infoText}>{word.article}</p>
              </div>

              <div>
                <p style={styles.smallLabel}>Мн. число</p>
                <p style={styles.infoText}>{word.plural}</p>
              </div>
            </div>
          </>
        )}
      </div>

      <div style={styles.buttons}>
        <button style={styles.secondaryButton} onClick={prev}>
          Назад
        </button>

        <button style={styles.mainButton} onClick={() => setShow(!show)}>
          Перевернуть
        </button>

        <button style={styles.secondaryButton} onClick={next}>
          Дальше
        </button>
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
    padding: "24px",
    boxSizing: "border-box",
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
    fontSize: 34,
    margin: 0,
  },

  counter: {
    fontSize: 20,
    color: "#cbd5e1",
    margin: 0,
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

  progressOuter: {
    maxWidth: 700,
    height: 10,
    background: "#334155",
    borderRadius: 999,
    margin: "0 auto 32px",
    overflow: "hidden",
  },

  progressInner: {
    height: "100%",
    background: "#38bdf8",
    borderRadius: 999,
    transition: "width 0.3s ease",
  },

  card: {
    maxWidth: 700,
    minHeight: 420,
    margin: "0 auto",
    background: "#78aee1",
    borderRadius: 28,
    boxShadow: "0 20px 60px rgba(0,0,0,0.35)",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    textAlign: "center",
    padding: 32,
    cursor: "pointer",
    boxSizing: "border-box",
  },

  label: {
    fontSize: 20,
    color: "#2e343d",
    marginBottom: 24,
  },

  mainWord: {
    fontSize: 44,
    fontWeight: 800,
    lineHeight: 1.1,
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
  },

  buttons: {
    maxWidth: 700,
    margin: "32px auto 0",
    display: "grid",
    gridTemplateColumns: "1fr 1.4fr 1fr",
    gap: 12,
  },

  mainButton: {
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
    padding: "10px 10px",
    borderRadius: 18,
    border: "1px solid #475569",
    background: "#1e293b",
    color: "white",
    fontSize: 20,
    fontWeight: 700,
    cursor: "pointer",
  },
};