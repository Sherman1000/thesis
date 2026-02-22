import ReactGA from 'react-ga'
import { LocalStorage } from './remote-api/localStorage'

const exercisesCategory = 'Exercises'
const userCategory = 'User'
const correctionsCategory = 'Corrections'
const contentCategory = 'Content'

// Initialization
export const initialize = () => ReactGA.initialize('UA-222467217-1')
export const initializeUser = () =>
  ReactGA.set({ userId: LocalStorage.fetchUserId() })

// Location
export const logLocation = () =>
  ReactGA.set({
    page: window.location.pathname,
    label: LocalStorage.fetchUserId(),
  })

// Content
export const logPreviousContentNavigation = (from: string, to: string) =>
  ReactGA.event({
    category: contentCategory,
    action: 'Navigate to previous section',
    label: LocalStorage.fetchUserId(),
    dimension1: from,
    dimension2: to,
  })

export const logNextContentNavigation = (from: string, to: string) =>
  ReactGA.event({
    category: contentCategory,
    action: 'Navigate to next section',
    label: LocalStorage.fetchUserId(),
    dimension1: from,
    dimension2: to,
  })

// Exercises
export const logExerciseSubmission = () =>
  ReactGA.event({
    category: exercisesCategory,
    action: 'Exercise submissions successfully loaded',
    label: LocalStorage.fetchUserId(),
  })

export const logExerciseSubmissionError = () =>
  ReactGA.exception({
    category: exercisesCategory,
    description: 'An error occurred when submitting exercise',
    label: LocalStorage.fetchUserId(),
  })

export const logEvaluationQuestions = () =>
  ReactGA.event({
    category: exercisesCategory,
    action: 'Evaluation questions successfully loaded',
    label: LocalStorage.fetchUserId(),
  })

export const logEvaluationQuestionsError = () =>
  ReactGA.exception({
    category: exercisesCategory,
    description: 'An error occurred when loading questions',
    label: LocalStorage.fetchUserId(),
  })

export const logEvaluation = () =>
  ReactGA.event({
    category: exercisesCategory,
    action: 'Unit submission',
    label: LocalStorage.fetchUserId(),
  })

export const logEvaluationError = () =>
  ReactGA.exception({
    category: exercisesCategory,
    description: 'An error occurred when submitting unit',
    label: LocalStorage.fetchUserId(),
  })

// User
export const logUserSignUpError = () =>
  ReactGA.exception({
    category: userCategory,
    description: 'An error occurred when signing up user',
    label: LocalStorage.fetchUserId(),
  })

export const logUserLogin = () =>
  ReactGA.event({
    category: userCategory,
    action: 'Logged in',
    label: LocalStorage.fetchUserId(),
  })

export const logUserLoginError = () =>
  ReactGA.exception({
    category: userCategory,
    description: 'An error occurred when logging user',
    label: LocalStorage.fetchUserId(),
  })

export const logUserLogOut = () =>
  ReactGA.event({
    category: userCategory,
    action: 'Logged out',
    label: LocalStorage.fetchUserId(),
  })

export const logUserLogOutError = () =>
  ReactGA.exception({
    category: userCategory,
    description: 'An error occurred when logging out user',
    label: LocalStorage.fetchUserId(),
  })

export const logSignUp = () =>
  ReactGA.event({
    category: userCategory,
    action: 'Created an Account',
    label: LocalStorage.fetchUserId(),
  })

// Corrections
export const logCorrections = () =>
  ReactGA.event({
    category: correctionsCategory,
    action: 'Unit corrections successfully loaded',
    label: LocalStorage.fetchUserId(),
  })

export const logCorrectionsError = () =>
  ReactGA.exception({
    category: correctionsCategory,
    description: 'Unit corrections failed to load',
    label: LocalStorage.fetchUserId(),
  })

export const logPeerCorrections = () =>
  ReactGA.event({
    category: correctionsCategory,
    action: 'Peer corrections successfully loaded',
    label: LocalStorage.fetchUserId(),
  })

export const logPeerCorrectionsError = () =>
  ReactGA.exception({
    category: correctionsCategory,
    description: 'Peer corrections failed to load',
    label: LocalStorage.fetchUserId(),
  })

export const logPendingPeerReview = () =>
  ReactGA.event({
    category: correctionsCategory,
    action: 'Pending peer reviews successfully loaded',
    label: LocalStorage.fetchUserId(),
  })

export const logPendingPeerReviewError = () =>
  ReactGA.exception({
    category: correctionsCategory,
    description: 'Pending peer reviews failed to load',
    label: LocalStorage.fetchUserId(),
  })

export const logPeerReviewSubmission = () =>
  ReactGA.event({
    category: correctionsCategory,
    action: 'Peer review submitted successfully',
    label: LocalStorage.fetchUserId(),
  })

export const logPeerReviewSubmissionError = () =>
  ReactGA.exception({
    category: correctionsCategory,
    description: 'Peer review failed to submit',
    label: LocalStorage.fetchUserId(),
  })

export const logAutomaticCorrections = () =>
  ReactGA.event({
    category: correctionsCategory,
    action: 'Automatic corrections successfully loaded',
    label: LocalStorage.fetchUserId(),
  })

export const logAutomaticCorrectionsError = () =>
  ReactGA.exception({
    category: correctionsCategory,
    description: 'Automatic corrections failed to load',
    label: LocalStorage.fetchUserId(),
  })

export const logStudents = () =>
  ReactGA.event({
    category: correctionsCategory,
    action: 'Students list successfully loaded',
    label: LocalStorage.fetchUserId(),
  })

export const logStudentsError = () =>
  ReactGA.exception({
    category: correctionsCategory,
    description: 'Students list failed to load',
    label: LocalStorage.fetchUserId(),
  })
