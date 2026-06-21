import { createContext, useContext, useState, useCallback } from 'react'
import { DEFAULT_LANG, LANGUAGES, t as translate } from './translations'

const LS_KEY = 'mochi_lang'

function storedLang() {
  try {
    const v = localStorage.getItem(LS_KEY)
    return LANGUAGES.includes(v) ? v : DEFAULT_LANG  // drop a stale 'ja'
  } catch { return DEFAULT_LANG }
}

const LanguageContext = createContext(null)

export function LanguageProvider({ children }) {
  const [lang, setLangState] = useState(storedLang)

  const setLang = useCallback(code => {
    setLangState(code)
    try { localStorage.setItem(LS_KEY, code) } catch { /* localStorage unavailable */ }
  }, [])

  const t = useCallback((key, vars) => translate(key, lang, vars), [lang])

  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  )
}

// eslint-disable-next-line react-refresh/only-export-components -- hook colocated with its provider by design
export function useLanguage() {
  return useContext(LanguageContext)
}
