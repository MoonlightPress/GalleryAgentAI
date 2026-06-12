import { useState, useEffect, useCallback } from 'react'

// Hash router: '#/mochi' | '#/saffron' | '#/peppercorn'
// Gives real URLs, working back button, and refresh-safe pages with zero deps.

const PAGES = ['mochi', 'saffron', 'peppercorn']

function parseHash() {
  const h = window.location.hash.replace(/^#\/?/, '').split('?')[0]
  return PAGES.includes(h) ? h : 'mochi'
}

export function useHashRoute() {
  const [page, setPage] = useState(parseHash)

  useEffect(() => {
    const onHash = () => setPage(parseHash())
    window.addEventListener('hashchange', onHash)
    return () => window.removeEventListener('hashchange', onHash)
  }, [])

  const navigate = useCallback(next => {
    if (PAGES.includes(next)) window.location.hash = `/${next}`
  }, [])

  return [page, navigate]
}
