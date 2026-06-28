import { useState, useEffect } from "react";

function shuffleArray(array) {
  const arr = [...array];

  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }

  return arr;
}

const GERMAN_VOICE_PREFERENCES = [
  "Petra",
  "Google Deutsch",
  "Anna",
  "Markus",
  "Yannick",
  "Siri",
  "Microsoft Katja",
  "Microsoft Conrad",
];

function getBestGermanVoice(voices) {
  const germanVoices = voices.filter((voice) => voice.lang?.toLowerCase().startsWith("de"));

  if (germanVoices.length === 0) {
    return null;
  }

  return (
    GERMAN_VOICE_PREFERENCES
      .map((preferredName) =>
        germanVoices.find((voice) => voice.name.toLowerCase().includes(preferredName.toLowerCase())),
      )
      .find(Boolean) || germanVoices.find((voice) => voice.lang === "de-DE") || germanVoices[0]
  );
}

const WORD_TOPICS = [
  { value: "Familie", label: "Familie (Семья)" },
  { value: "Haus und Möbel", label: "Haus und Möbel (Дом и мебель)" },
  { value: "Essen und Trinken", label: "Essen und Trinken (Еда и напитки)" },
  { value: "Kleidung und Schuhe", label: "Kleidung und Schuhe (Одежда и обувь)" },
  { value: "Körper und Gesundheit", label: "Körper und Gesundheit (Тело и здоровье)" },
  { value: "Arbeit und Berufe", label: "Arbeit und Berufe (Работа и профессии)" },
  { value: "Schule und Bildung", label: "Schule und Bildung (Учёба и образование)" },
  { value: "Einkaufen und Geld", label: "Einkaufen und Geld (Покупки и деньги)" },
  { value: "Verkehr", label: "Verkehr (Транспорт)" },
  { value: "Reisen", label: "Reisen (Путешествия)" },
  { value: "Stadt und Infrastruktur", label: "Stadt und Infrastruktur (Город и инфраструктура)" },
  { value: "Natur und Umwelt", label: "Natur und Umwelt (Природа и окружающий мир)" },
  { value: "Tiere", label: "Tiere (Животные)" },
  { value: "Zeit und Datum", label: "Zeit und Datum (Время и даты)" },
  { value: "Wetter und Jahreszeiten", label: "Wetter und Jahreszeiten (Погода и сезоны)" },
  { value: "Hobbys und Freizeit", label: "Hobbys und Freizeit (Хобби и свободное время)" },
  { value: "Sport und Bewegung", label: "Sport und Bewegung (Спорт и активность)" },
  { value: "Gefühle und Emotionen", label: "Gefühle und Emotionen (Чувства и эмоции)" },
  { value: "Kommunikation und Beziehungen", label: "Kommunikation und Beziehungen (Общение и отношения)" },
  { value: "Technik und Technologie", label: "Technik und Technologie (Технологии и техника)" },
  { value: "Парные слова", label: "Парные слова (Wortpaare)" },
  { value: "Предлоги", label: "Предлоги (Präpositionen)" },
];

export default function App() {
  const [words, setWords] = useState([]);
  const [verbs, setVerbs] = useState([]);
  const [phrases, setPhrases] = useState([]);
  const [mode, setMode] = useState("words");
  

  const [index, setIndex] = useState(0);
  const [show, setShow] = useState(false);

  const [selectedArticle, setSelectedArticle] = useState("all");
  const [selectedLevel, setSelectedLevel] = useState("all");
  const [selectedTopic, setSelectedTopic] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [speechVoices, setSpeechVoices] = useState([]);

  // Article-check (Проверки) state
  const ARTICLE_MISTAKES_KEY = "deutschTrainer.articleMistakes.v1";
  const [articleMistakes, setArticleMistakes] = useState(() => {
    if (typeof window === "undefined") return [];
    try {
      const raw = window.localStorage.getItem(ARTICLE_MISTAKES_KEY);
      const parsed = raw ? JSON.parse(raw) : [];
      return Array.isArray(parsed) ? parsed.filter((x) => typeof x === "string") : [];
    } catch (error) {
      return [];
    }
  });
  const [articleIndex, setArticleIndex] = useState(0);
  const [articlePhase, setArticlePhase] = useState("quiz");
  const [articlePicked, setArticlePicked] = useState(null);

  useEffect(() => {
    if (typeof window === "undefined") return;
    try {
      window.localStorage.setItem(ARTICLE_MISTAKES_KEY, JSON.stringify(articleMistakes));
    } catch (error) {
      // ignore
    }
  }, [articleMistakes]);

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

  useEffect(() => {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) {
      return undefined;
    }

    const loadVoices = () => {
      setSpeechVoices(window.speechSynthesis.getVoices());
    };

    loadVoices();
    window.speechSynthesis.addEventListener("voiceschanged", loadVoices);

    return () => {
      window.speechSynthesis.removeEventListener("voiceschanged", loadVoices);
    };
  }, []);

  const filteredWordsByControls = words.filter((word) => {
    const matchesArticle = selectedArticle === "all" || word.article === selectedArticle;
    const matchesTopic = selectedTopic === "all" || word.topic === selectedTopic;

    return matchesArticle && matchesTopic;
  });

  const filteredVerbsByControls = verbs.filter((verb) => {
  return selectedLevel === "all" || verb.level === selectedLevel;
  });

  const normalizedSearchQuery = searchQuery.trim().toLowerCase();

  function matchesSearch(item, fields) {
    if (!normalizedSearchQuery) {
      return true;
    }

    return fields.some((field) => String(item[field] || "").toLowerCase().includes(normalizedSearchQuery));
  }

  const filteredWords = filteredWordsByControls.filter((word) =>
    matchesSearch(word, ["de", "ru", "plural", "article", "topic", "case", "note", "example_de", "example_ru"]),
  );

  const filteredVerbs = filteredVerbsByControls.filter((verb) =>
    matchesSearch(verb, ["de", "infinitive", "ru", "level", "example_de", "example_ru"]),
  );

  const filteredPhrases = phrases.filter((phrase) =>
    matchesSearch(phrase, ["de", "ru", "example_de", "example_ru"]),
  );


  // Article-check (Проверки) list: only words with a real article (der/die/das).
  const articleEligibleWords = words.filter((word) => {
    const a = String(word.article || "").trim().toLowerCase();
    return a === "der" || a === "die" || a === "das";
  });

  // Strip leading article from a word's `de` field (e.g. "der Apfel" -> "Apfel").
  function stripArticle(de) {
    const text = String(de || "").trim();
    return text.replace(/^(der|die|das)\s+/i, "");
  }

  // Mistakes first (in saved order), then the rest of the eligible pool in stable order.
  const mistakeSet = new Set(articleMistakes);
  const articleList = [
    ...articleEligibleWords.filter((w) => mistakeSet.has(w.de)),
    ...articleEligibleWords.filter((w) => !mistakeSet.has(w.de)),
  ];


  const currentList =
  mode === "words"
    ? filteredWords
    : mode === "verbs"
    ? filteredVerbs
    : filteredPhrases;

  const isLoading =
    (mode === "words" && words.length === 0) ||
    (mode === "verbs" && verbs.length === 0) ||
    (mode === "phrases" && phrases.length === 0);

  if (isLoading) {
    return <div style={styles.loading}>Загрузка...</div>;
  }

  const item = currentList[index];
  const isPhone = typeof window !== "undefined" && window.innerWidth <= 480;

  function next() {
    if (currentList.length === 0) {
      return;
    }

    setShow(false);
    setIndex((prev) => (prev + 1) % currentList.length);
  }

  function prev() {
    if (currentList.length === 0) {
      return;
    }

    setShow(false);
    setIndex((prev) => (prev - 1 + currentList.length) % currentList.length);
  }

  function getSpeechText(card) {
    if (!card) {
      return "";
    }

    if (mode === "words") {
      const plural = String(card.plural || "").trim();

      if (show && plural && plural !== "—" && plural !== "-") {
        return plural;
      }

      const word = card.de || "";
      const alreadyHasArticle = /^(der|die|das)\s/i.test(word);

      return alreadyHasArticle ? word : [card.article, word].filter(Boolean).join(" ");
    }

    if (mode === "phrases") {
      return show ? card.example_de || card.de || "" : card.de || "";
    }

    return card.infinitive || card.de || "";
  }

  function speakGerman(event) {
    event.stopPropagation();

    const text = getSpeechText(item);

    if (!text || typeof window === "undefined" || !("speechSynthesis" in window)) {
      return;
    }

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    const germanVoice = getBestGermanVoice(speechVoices);

    utterance.lang = germanVoice?.lang || "de-DE";
    utterance.rate = 0.9;
    utterance.pitch = 1;

    if (germanVoice) {
      utterance.voice = germanVoice;
    }

    window.speechSynthesis.speak(utterance);
  }

  function changeMode(newMode) {
  setMode(newMode);
  setIndex(0);
  setShow(false);
  setSearchQuery("");

  if (newMode === "words") {
    setSelectedLevel("all");
  }

  if (newMode === "verbs") {
    setSelectedArticle("all");
    setSelectedTopic("all");
  }

  if (newMode === "articles") {
    setSelectedArticle("all");
    setSelectedTopic("all");
    setSelectedLevel("all");
    setArticleIndex(0);
    setArticlePhase("quiz");
    setArticlePicked(null);
  }
}

  return (
    <div style={{ ...styles.page, ...(isPhone ? styles.phonePage : {}) }}>
      <div style={{ ...styles.header, ...(isPhone ? styles.phoneHeader : {}) }}>
        <h1 style={{ ...styles.title, ...(isPhone ? styles.phoneTitle : {}) }}>Deutsch Trainer</h1>

        <p style={{ ...styles.counter, ...(isPhone ? styles.phoneCounter : {}) }}>
          {mode === "articles"
            ? "Проверка артиклей"
            : `${currentList.length > 0 ? index + 1 : 0} / ${currentList.length}`}
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

        <button
          style={
            mode === "articles"
              ? { ...styles.activeModeButton, ...(isPhone ? styles.phoneModeButton : {}) }
              : { ...styles.modeButton, ...(isPhone ? styles.phoneModeButton : {}) }
          }
          onClick={() => changeMode("articles")}
        >
          Проверки
        </button>
          </div>

      {mode === "words" && (
        <div style={{ ...styles.articleButtons, ...(isPhone ? styles.phoneArticleButtons : {}) }}>
          <select
            value={selectedTopic}
            style={{ ...styles.topicSelect, ...(isPhone ? styles.phoneTopicSelect : {}) }}
            onChange={(event) => {
              setSelectedTopic(event.target.value);
              setIndex(0);
              setShow(false);
            }}
            aria-label="Темы"
          >
            <option value="all">Темы</option>
            {WORD_TOPICS.map((topic) => (
              <option key={topic.value} value={topic.value}>
                {topic.label}
              </option>
            ))}
          </select>

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

      {mode === "articles" && (
        <ArticleCheckView
          list={articleList}
          index={articleIndex}
          phase={articlePhase}
          picked={articlePicked}
          isPhone={isPhone}
          mistakesCount={articleMistakes.length}
          stripArticle={stripArticle}
          onPick={(article) => {
            if (articlePhase !== "quiz") return;
            const word = articleList[articleIndex];
            if (!word) return;
            const correct = String(word.article || "").toLowerCase();
            setArticlePicked(article);
            if (article !== correct) {
              setArticleMistakes((prev) =>
                prev.includes(word.de) ? prev : [...prev, word.de],
              );
            }
            setArticlePhase("reveal");
          }}
          onNext={() => {
            if (articleList.length === 0) return;
            setArticlePicked(null);
            setArticlePhase("quiz");
            setArticleIndex((prev) => (prev + 1) % articleList.length);
          }}
          onClearMistakes={() => setArticleMistakes([])}
        />
      )}

      <div style={mode === "articles" ? { display: "none" } : undefined}>
      <div style={styles.progressOuter}>
        <div
          style={{
            ...styles.progressInner,
            width: currentList.length > 0 ? `${((index + 1) / currentList.length) * 100}%` : "0%",
          }}
        />
      </div>

      <form
        style={{ ...styles.searchForm, ...(isPhone ? styles.phoneSearchForm : {}) }}
        onSubmit={(event) => event.preventDefault()}
      >
        <input
          type="search"
          value={searchQuery}
          placeholder="Search words..."
          aria-label="Search words"
          style={{ ...styles.searchInput, ...(isPhone ? styles.phoneSearchInput : {}) }}
          onChange={(event) => {
            setSearchQuery(event.target.value);
            setIndex(0);
            setShow(false);
          }}
        />
      </form>

      {currentList.length === 0 ? (
        <div style={{ ...styles.card, ...styles.frontCard, ...(isPhone ? styles.phoneCard : {}) }}>
          <div style={{ ...styles.emptyText, ...(isPhone ? styles.phoneEmptyText : {}) }}>
            Нет слов по выбранным фильтрам
          </div>
        </div>
      ) : (
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
          <button
              type="button"
              style={{ ...styles.soundButton, ...(isPhone ? styles.phoneSoundButton : {}) }}
              onClick={speakGerman}
              aria-label="Озвучить по-немецки"
              title="Озвучить по-немецки"
            >
              🔊
            </button>

          {!show ? (
           <>
  <div style={{ ...styles.mainWord, ...styles.frontMainWord, ...(isPhone ? styles.phoneFrontMainWord : {}) }}>
    {mode === "words"
      ? item.de
      : mode === "verbs"
      ? item.infinitive || item.de
      : item.de}
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
                  <p style={styles.smallLabel}>{item.case ? "Падеж / вопрос" : "Артикль"}</p>
                  <p style={styles.infoText}>{item.case || item.article}</p>
                </div>

                <div>
                  <p style={styles.smallLabel}>{item.note ? "Важно" : "Мн. число"}</p>
                  <p style={styles.infoText}>{item.note || item.plural}</p>
                </div>
              </div>

              {item.example_de && (
                <div style={{ ...styles.exampleBox, ...(isPhone ? styles.phoneExampleBox : {}) }}>
                  <p style={{ ...styles.exampleDe, ...(isPhone ? styles.phoneExampleDe : {}) }}>{item.example_de}</p>
                  <p style={{ ...styles.exampleRu, ...(isPhone ? styles.phoneExampleRu : {}) }}>{item.example_ru}</p>
                </div>
              )}
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
              <div style={{ ...styles.mainWord, ...(isPhone ? styles.phoneMainWord : {}) }}>{item.ru}</div>

              <div style={{ ...styles.exampleBox, ...(isPhone ? styles.phoneExampleBox : {}) }}>
                <p style={{ ...styles.exampleDe, ...(isPhone ? styles.phoneExampleDe : {}) }}>{item.example_de}</p>
                <p style={{ ...styles.exampleRu, ...(isPhone ? styles.phoneExampleRu : {}) }}>{item.example_ru}</p>
              </div>
            </>
          )}
        </div>
      )}

        {currentList.length > 0 && (
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
        )}
      </div>
      </div>
    </div>
  );
}


const styles = {
  page: {
  minHeight: "100svh",
  background: "#F5F6F8",
  color: "#203142",
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
    background: "#F5F6F8",
    color: "#203142",
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
  display: "grid",
  gridTemplateColumns: "1fr auto 1fr",
  alignItems: "center",
},

  title: {
    fontSize: "clamp(24px, 4.5vw, 46px)",
    gridColumn: 2,
    margin: 0,
    fontWeight: 900,
    textAlign: "center",
    color: "#6B7280",
  },

  counter: {
    fontSize: 16,
    color: "#6B7280",
    gridColumn: 3,
    justifySelf: "end",
    margin: 0,
  },

  modeButtons: {
  width: "100%",
  maxWidth: 700,
  margin: "14px auto 18px",
  display: "grid",
  gridTemplateColumns: "1fr 1fr 1fr 1fr",
  gap: 10,
},

modeButton: {
  padding: "13px 8px",
  borderRadius: 18,
  border: "1px solid #D8DCE3",
  background: "#F7F7F8",
  color: "#374151",
  fontSize: "clamp(14px, 3.5vw, 20px)",
  fontWeight: 700,
  cursor: "pointer",
  whiteSpace: "nowrap",
},

activeModeButton: {
  padding: "13px 8px",
  borderRadius: 18,
  border: "1px solid #4F6D8A",
  background: "#4F6D8A",
  color: "#FFFFFF",
  fontSize: "clamp(14px, 3.5vw, 20px)",
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
  border: "1px solid #D8DCE3",
  background: "#F7F7F8",
  color: "#374151",
  fontSize: 16,
  fontWeight: 500,
  cursor: "pointer",
},

activeArticleButton: {
  padding: "10px 18px",
  borderRadius: 999,
  border: "1px solid #4F6D8A",
  background: "#4F6D8A",
  color: "#FFFFFF",
  fontSize: 16,
  fontWeight: 700,
  cursor: "pointer",
},

topicSelect: {
  minHeight: 42,
  maxWidth: 260,
  padding: "10px 38px 10px 18px",
  borderRadius: 999,
  border: "1px solid #D8DCE3",
  background: "#F7F7F8",
  color: "#374151",
  fontSize: 16,
  fontWeight: 700,
  cursor: "pointer",
},

searchForm: {
  width: "100%",
  maxWidth: 700,
  margin: "0 auto 14px",
  display: "flex",
  justifyContent: "center",
},

searchInput: {
  width: "min(100%, 300px)",
  minHeight: 42,
  padding: "10px 18px",
  borderRadius: 999,
  border: "1px solid #D8DCE3",
  background: "#F7F7F8",
  color: "#374151",
  fontSize: 16,
  fontWeight: 700,
  outline: "none",
  boxSizing: "border-box",
},

  card: {
  width: "100%",
  maxWidth: 700,
  margin: "0 auto",
  background: "#FCFCFC",
  borderRadius: 28,
  boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
  textAlign: "center",
  cursor: "pointer",
  boxSizing: "border-box",
  position: "relative",
},

soundButton: {
  position: "absolute",
  top: 14,
  right: 14,
  width: 44,
  height: 44,
  borderRadius: 999,
  border: "1px solid #D8DCE3",
  background: "#F7F7F8",
  color: "#203142",
  fontSize: 20,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  cursor: "pointer",
  boxShadow: "0 2px 6px rgba(0,0,0,0.06)",
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
  color: "#203142",
},

frontMainWord: {
  fontSize: "clamp(34px, 5.6vw, 46px)",
  letterSpacing: "0.01em",
},

hint: {
  marginTop: 14,
  fontSize: 17,
  color: "#6B7280",
},

infoBox: {
  marginTop: 28,
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: 20,
  width: "100%",
},

smallLabel: {
  color: "#6B7280",
  fontSize: 16,
  marginBottom: 8,
},

infoText: {
  fontSize: 24,
  fontWeight: 700,
  margin: 0,
  color: "#203142",
},

emptyText: {
  fontSize: 24,
  fontWeight: 800,
  color: "#203142",
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
  background: "rgba(255,255,255,0.45)",
  borderRadius: 14,
  padding: "7px 14px",
  fontSize: 17,
},

person: {
  fontWeight: 700,
  color: "#6B7280",
},

form: {
  fontWeight: 800,
  color: "#203142",
},

exampleBox: {
  marginTop: 18,
  background: "rgba(255,255,255,0.45)",
  borderRadius: 18,
  padding: 14,
  width: "100%",
  maxWidth: 520,
},

exampleDe: {
  fontSize: 16,
  fontWeight: 800,
  margin: "0 0 8px",
  color: "#203142",
},

exampleRu: {
  fontSize: 16,
  margin: 0,
  color: "#6B7280",
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
  border: "1px solid #4F6D8A",
  background: "#4F6D8A",
  color: "#FFFFFF",
  fontSize: "clamp(14px, 3.5vw, 20px)",
  fontWeight: 700,
  cursor: "pointer",
  whiteSpace: "nowrap",
},

secondaryButton: {
  padding: "13px 8px",
  borderRadius: 18,
  border: "1px solid #D8DCE3",
  background: "#F7F7F8",
  color: "#374151",
  fontSize: "clamp(14px, 3.5vw, 20px)",
  fontWeight: 700,
  cursor: "pointer",
  whiteSpace: "nowrap",
},

caseBox: {
  marginTop: 18,
  padding: "10px 16px",
  borderRadius: 999,
  background: "rgba(255,255,255,0.45)",
  color: "#203142",
  fontSize: 16,
  fontWeight: 700,
},

frontCaseBox: {
  marginTop: 28,
  padding: "12px 22px",
  borderRadius: 999,
  background: "rgba(255,255,255,0.45)",
  color: "#203142",
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
  border: "1px solid #D8DCE3",
  background: "#F7F7F8",
  color: "#374151",
  fontSize: 16,
  cursor: "pointer",
},

activeLevelButton: {
  padding: "10px 16px",
  borderRadius: 999,
  border: "1px solid #4F6D8A",
  background: "#4F6D8A",
  color: "#FFFFFF",
  fontSize: 16,
  fontWeight: 700,
  cursor: "pointer",
},

phonePage: {
  minHeight: "100dvh",
  padding: "14px 8px 18px",
  overflowY: "hidden",
},

phoneHeader: {
  margin: "0 auto 12px",
},

phoneTitle: {
  fontSize: 33,
  lineHeight: 1.1,
},

phoneCounter: {
  fontSize: 15,
},

phoneModeButtons: {
  margin: "10px auto 14px",
  gap: 8,
},

phoneModeButton: {
  padding: "11px 6px",
  borderRadius: 16,
  fontSize: 16,
},

phoneArticleButtons: {
  margin: "0 auto 12px",
  gap: 4,
  flexWrap: "nowrap",
  alignItems: "center",
  justifyContent: "center",
},

phoneLevelButtons: {
  margin: "0 auto 12px",
  gap: 6,
  flexWrap: "nowrap",
},

phoneFilterButton: {
  padding: "7px 10px",
  fontSize: 18,
  flex: "0 0 auto",
},

phoneTopicSelect: {
  width: 122,
  minWidth: 122,
  maxWidth: 122,
  minHeight: 38,
  padding: "7px 28px 7px 12px",
  fontSize: 18,
  flex: "0 0 auto",
},

phoneSearchForm: {
  margin: "0 auto 10px",
  padding: "0 4px",
},

phoneSearchInput: {
  width: "min(100%, 240px)",
  minHeight: 38,
  padding: "8px 14px",
  fontSize: 16,
},

phoneCard: {
  maxWidth: "100%",
  borderRadius: 24,
},

phoneSoundButton: {
  top: 10,
  right: 10,
  width: 40,
  height: 40,
  fontSize: 18,
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
  margin: "14px auto 0",
  gap: 8,
},

phoneNavButton: {
  padding: "11px 6px",
  borderRadius: 16,
  fontSize: 16,
},

progressOuter: {
  width: "100%",
  maxWidth: 700,
  height: 6,
  borderRadius: 999,
  background: "#E3E6EC",
  overflow: "hidden",
  margin: "0 auto 14px",
},

progressInner: {
  height: "100%",
  background: "#4F6D8A",
  borderRadius: 999,
  transition: "width 0.2s ease",
},

articleMistakesBar: {
  width: "100%",
  maxWidth: 700,
  margin: "0 auto 14px",
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  gap: 10,
  color: "#6B7280",
  fontSize: 15,
  fontWeight: 700,
},

articleCard: {
  width: "100%",
  maxWidth: 700,
  margin: "0 auto",
  minHeight: "clamp(220px, 27svh, 280px)",
  padding: "28px 22px",
  background: "#FCFCFC",
  borderRadius: 28,
  boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "stretch",
  textAlign: "center",
  boxSizing: "border-box",
  position: "relative",
},

phoneArticleCard: {
  padding: "22px 16px",
  minHeight: "clamp(180px, 24dvh, 230px)",
  borderRadius: 24,
},

articleMistakesClearButton: {
  padding: "8px 12px",
  borderRadius: 999,
  fontSize: 14,
  whiteSpace: "nowrap",
},

articleChoiceRow: {
  marginTop: 22,
  display: "grid",
  gridTemplateColumns: "1fr 1fr 1fr",
  gap: 10,
  width: "100%",
},

articleChoiceButton: {
  padding: "12px 6px",
  borderRadius: 18,
  border: "1px solid #4F6D8A",
  background: "#4F6D8A",
  color: "#FFFFFF",
  fontSize: "clamp(18px, 3.5vw, 22px)",
  fontWeight: 800,
  cursor: "pointer",
  whiteSpace: "nowrap",
},

articleReveal: {
  marginTop: 18,
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  gap: 6,
},

articleRevealBadge: {
  display: "inline-block",
  padding: "8px 16px",
  borderRadius: 999,
  fontSize: 16,
  fontWeight: 800,
},

articleRevealBadgeWrong: {
  background: "#FBE3E3",
  color: "#9B1C1C",
  border: "1px solid #F2B5B5",
},

articleRevealBadgeRight: {
  background: "#DCEFE0",
  color: "#1F6B3A",
  border: "1px solid #B7DBC0",
},

articleRevealHint: {
  fontSize: 14,
  color: "#6B7280",
  textAlign: "center",
  maxWidth: 420,
},

phoneProgressOuter: {
  margin: "0 auto 10px",
},

phoneArticleMistakesBar: {
  flexDirection: "column",
  alignItems: "stretch",
  gap: 6,
  fontSize: 14,
  margin: "0 auto 10px",
},

phoneArticleHint: {
  fontSize: 15,
  marginTop: 10,
},

phoneArticleChoiceRow: {
  marginTop: 16,
  gap: 8,
},

phoneArticleChoiceButton: {
  padding: "10px 4px",
  fontSize: 18,
  borderRadius: 16,
},

phoneArticleReveal: {
  marginTop: 14,
},
};


function ArticleCheckView({
  list,
  index,
  phase,
  picked,
  isPhone,
  mistakesCount,
  stripArticle,
  onPick,
  onNext,
  onClearMistakes,
}) {
  const ARTICLES = ["der", "die", "das"];

  if (list.length === 0) {
    return (
      <div style={{ ...styles.card, ...(isPhone ? styles.phoneCard : {}) }}>
        <div style={{ ...styles.emptyText, ...(isPhone ? styles.phoneEmptyText : {}) }}>
          Нет слов с известным артиклем для проверки
        </div>
      </div>
    );
  }

  const word = list[index];
  const correct = String(word.article || "").toLowerCase();
  const isCorrectPick = picked === correct;
  const isMistake = phase === "reveal" && !isCorrectPick;
  const bare = stripArticle(word.de);

  return (
    <>
      <div style={{ ...styles.progressOuter, ...(isPhone ? styles.phoneProgressOuter : {}) }}>
        <div
          style={{
            ...styles.progressInner,
            width: list.length > 0 ? `${((index + 1) / list.length) * 100}%` : "0%",
          }}
        />
      </div>

      <div style={{ ...styles.articleMistakesBar, ...(isPhone ? styles.phoneArticleMistakesBar : {}) }}>
        <span>
          Слово {list.length > 0 ? index + 1 : 0} / {list.length}
          {mistakesCount > 0 ? ` · На повторении: ${mistakesCount}` : ""}
        </span>
        {mistakesCount > 0 && (
          <button
            type="button"
            style={{ ...styles.secondaryButton, ...styles.articleMistakesClearButton, ...(isPhone ? styles.phoneNavButton : {}) }}
            onClick={onClearMistakes}
            title="Убрать все слова из повторения"
          >
            Очистить повтор
          </button>
        )}
      </div>

      {phase === "quiz" ? (
        <div style={{ ...styles.articleCard, ...(isPhone ? styles.phoneArticleCard : {}) }}>
          <div style={{ ...styles.mainWord, ...styles.frontMainWord, ...(isPhone ? styles.phoneFrontMainWord : {}) }}>
            {bare}
          </div>
          <div style={{ ...styles.hint, ...(isPhone ? styles.phoneArticleHint : {}) }}>
            Выбери правильный артикль
          </div>
          <div style={{ ...styles.articleChoiceRow, ...(isPhone ? styles.phoneArticleChoiceRow : {}) }}>
            {ARTICLES.map((article) => (
              <button
                key={article}
                type="button"
                style={{ ...styles.articleChoiceButton, ...(isPhone ? styles.phoneArticleChoiceButton : {}) }}
                onClick={() => onPick(article)}
              >
                {article}
              </button>
            ))}
          </div>
        </div>
      ) : (
        <div
          style={{
            ...styles.articleCard,
            ...(isPhone ? styles.phoneArticleCard : {}),
          }}
        >
          <div style={{ ...styles.mainWord, ...(isPhone ? styles.phoneMainWord : {}) }}>
            {word.de}
          </div>

          <div style={{ ...styles.infoBox, ...(isPhone ? styles.phoneInfoBox : {}) }}>
            <div>
              <p style={styles.smallLabel}>Артикль</p>
              <p style={styles.infoText}>{word.article}</p>
            </div>
            <div>
              <p style={styles.smallLabel}>Перевод</p>
              <p style={styles.infoText}>{word.ru}</p>
            </div>
          </div>

          <div style={{ ...styles.articleReveal, ...(isPhone ? styles.phoneArticleReveal : {}) }}>
            {isMistake ? (
              <>
                <span style={{ ...styles.articleRevealBadge, ...styles.articleRevealBadgeWrong }}>
                  Неверно: «{picked}»
                </span>
                <span style={{ ...styles.articleRevealHint }}>
                  Слово добавлено в повтор — увидишь его снова в начале списка.
                </span>
              </>
            ) : (
              <span style={{ ...styles.articleRevealBadge, ...styles.articleRevealBadgeRight }}>
                Верно!
              </span>
            )}
          </div>

          <div style={{ ...styles.buttons, ...(isPhone ? styles.phoneButtons : {}) }}>
            <span />
            <button
              type="button"
              style={{ ...styles.mainButton, ...(isPhone ? styles.phoneNavButton : {}) }}
              onClick={onNext}
            >
              Дальше
            </button>
            <span />
          </div>
        </div>
      )}
    </>
  );
}
