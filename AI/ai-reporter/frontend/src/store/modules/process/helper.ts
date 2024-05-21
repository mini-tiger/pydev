import { ss } from '@/utils/storage'

const LOCAL_NAME = 'GENERATE_PROCESS'

export function getLocalTabs() {
  return ss.get(LOCAL_NAME)
}

export function setLocalTabs(token: string) {
  return ss.set(LOCAL_NAME, token)
}

export function removeLocalTabs() {
  return ss.remove(LOCAL_NAME)
}
