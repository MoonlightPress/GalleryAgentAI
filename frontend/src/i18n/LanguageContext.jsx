import { createContext, useContext, useState, useCallback } from 'react'
import { DEFAULT_LANG, t as translate } from './translations'

const LS_KEY = 'mochi_lang'

function storedLang() {
  try { return localStorage.getItem(LS_KEY) || DEFAULT_LANG }
  catch { return DEFAULT_LANG }
}

const LanguageContext = createContext(null)

export function LanguageProvider({ children }) {
  const [lang, setLangState] = useState(storedLang)

  const setLang = useCallback(code => {
    setLangState(code)
    try { localStorage.setItem(LS_KEY, code) } catch {}
  }, [])

  const t = useCallback((key, vars) => translate(key, lang, vars), [lang])

  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  return useContext(LanguageContext)
}
