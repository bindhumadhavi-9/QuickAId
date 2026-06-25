import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft, Check, X, RotateCcw, Trophy, AlertTriangle } from 'lucide-react'

interface QuizQuestion {
  id: number
  question: string
  options: string[]
  correct: number
  explanation: string
}

const questions: QuizQuestion[] = [
  {
    id: 1,
    question: 'What should you do first when someone is bleeding heavily?',
    options: [
      'Apply a tourniquet immediately',
      'Apply direct pressure with a clean cloth',
      'Wait for the bleeding to stop on its own',
      'Elevate the wound above the heart',
    ],
    correct: 1,
    explanation: 'Direct pressure is the first and most important step. Tourniquets should only be used as a last resort for life-threatening bleeding that cannot be controlled by direct pressure.',
  },
  {
    id: 2,
    question: 'What is the correct treatment for a minor burn?',
    options: [
      'Apply ice directly to the burn',
      'Apply butter or oil to the burn',
      'Run cool (not cold) water over the burn for 10-20 minutes',
      'Break any blisters that form',
    ],
    correct: 2,
    explanation: 'Cool running water helps reduce tissue damage and pain. Ice can cause further damage, butter traps heat, and blisters protect against infection.',
  },
  {
    id: 3,
    question: 'What should you do if someone is choking but can still cough or speak?',
    options: [
      'Perform the Heimlich maneuver immediately',
      'Slap them on the back hard',
      'Encourage them to keep coughing',
      'Give them water to drink',
    ],
    correct: 2,
    explanation: 'If the person can cough or speak, their airway is partially open. Encouraging them to cough may dislodge the object. Perform abdominal thrusts only if they cannot breathe, cough, or speak.',
  },
  {
    id: 4,
    question: 'What is the correct position for someone who is unconscious but breathing normally?',
    options: [
      'Sit them upright',
      'Recovery position (on their side)',
      'Lie flat on their back',
      'Stand them up',
    ],
    correct: 1,
    explanation: 'The recovery position keeps the airway open and allows fluids to drain, preventing choking. Never leave an unconscious person flat on their back.',
  },
  {
    id: 5,
    question: 'When should you call emergency services for a suspected heart attack?',
    options: [
      'Only if the person loses consciousness',
      'After trying home remedies for 10 minutes',
      'Immediately when symptoms begin',
      'Only if chest pain is severe',
    ],
    correct: 2,
    explanation: 'Time is critical in heart attacks. Call emergency services immediately. Early treatment significantly improves outcomes. Never wait or try home remedies.',
  },
  {
    id: 6,
    question: 'What should you NOT do when someone has a suspected spinal injury?',
    options: [
      'Keep them still',
      'Move them unless absolutely necessary',
      'Keep their head and neck aligned',
      'Call for emergency help',
    ],
    correct: 1,
    explanation: 'Moving someone with a spinal injury can cause permanent paralysis. Keep them absolutely still and stabilize their head/neck until help arrives.',
  },
  {
    id: 7,
    question: 'For an electrical burn, what should you do first?',
    options: [
      'Touch the person to check responsiveness',
      'Turn off the power source or separate person from electricity',
      'Apply burn ointment',
      'Cover with a bandage',
    ],
    correct: 1,
    explanation: 'Never touch someone still in contact with electricity - you could be shocked too. Always disconnect the power source first or use a non-conductive object to separate them.',
  },
  {
    id: 8,
    question: 'What indicates a serious head injury requiring immediate medical attention?',
    options: [
      'Mild headache',
      'Small bump on forehead',
      'Clear fluid draining from nose or ears',
      'Feeling slightly dizzy for a few seconds',
    ],
    correct: 2,
    explanation: 'Clear fluid from nose or ears may indicate a skull fracture and brain injury. This is a medical emergency requiring immediate attention.',
  },
  {
    id: 9,
    question: 'How long should you perform CPR compressions?',
    options: [
      'Until you get tired',
      'For 5 minutes maximum',
      'Continue until emergency services arrive or person recovers',
      'Only if you have formal CPR training',
    ],
    correct: 2,
    explanation: 'Continue CPR until professional help arrives, the person starts breathing normally, or it becomes unsafe to continue. Even untrained responders can perform hands-only CPR.',
  },
  {
    id: 10,
    question: 'What is the correct ratio for CPR compressions to breaths?',
    options: [
      '15 compressions : 2 breaths',
      '30 compressions : 2 breaths',
      '10 compressions : 1 breath',
      '20 compressions : 3 breaths',
    ],
    correct: 1,
    explanation: 'The standard CPR ratio is 30 compressions to 2 rescue breaths for adults. Compressions should be at least 2 inches deep and at a rate of 100-120 per minute.',
  },
]

export default function Quiz() {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [showResult, setShowResult] = useState(false)
  const [score, setScore] = useState(0)
  const [answers, setAnswers] = useState<(number | null)[]>([])
  const [quizComplete, setQuizComplete] = useState(false)

  const question = questions[currentQuestion]
  const isCorrect = selectedAnswer === question.correct

  const handleAnswer = (answerIndex: number) => {
    if (showResult) return

    setSelectedAnswer(answerIndex)
    setShowResult(true)
    setAnswers([...answers, answerIndex])

    if (answerIndex === question.correct) {
      setScore(score + 1)
    }
  }

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
      setSelectedAnswer(null)
      setShowResult(false)
    } else {
      setQuizComplete(true)
    }
  }

  const handleRestart = () => {
    setCurrentQuestion(0)
    setSelectedAnswer(null)
    setShowResult(false)
    setScore(0)
    setAnswers([])
    setQuizComplete(false)
  }

  if (quizComplete) {
    const percentage = Math.round((score / questions.length) * 100)
    const isPassing = percentage >= 70

    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 text-center">
          <div
            className={`w-20 h-20 rounded-full mx-auto mb-4 flex items-center justify-center ${
              isPassing ? 'bg-green-100 dark:bg-green-900/30' : 'bg-amber-100 dark:bg-amber-900/30'
            }`}
          >
            {isPassing ? (
              <Trophy className="w-10 h-10 text-green-600 dark:text-green-400" />
            ) : (
              <AlertTriangle className="w-10 h-10 text-amber-600 dark:text-amber-400" />
            )}
          </div>

          <h1 className="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-2">
            {isPassing ? 'Great Job!' : 'Keep Learning!'}
          </h1>

          <p className="text-gray-600 dark:text-gray-400 mb-6">
            You scored {score} out of {questions.length} ({percentage}%)
          </p>

          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden mb-6">
            <div
              className={`h-full ${
                isPassing ? 'bg-green-500' : 'bg-amber-500'
              }`}
              style={{ width: `${percentage}%` }}
            />
          </div>

          <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">
            {isPassing
              ? 'You have a good understanding of basic first aid!'
              : 'Review the material and try again to improve your score.'}
          </p>

          <div className="space-y-3">
            <button
              onClick={handleRestart}
              className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium flex items-center justify-center gap-2 transition-colors"
            >
              <RotateCcw className="w-4 h-4" />
              Try Again
            </button>

            <Link
              to="/"
              className="block w-full py-3 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg font-medium hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            >
              Back to Home
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <header className="bg-purple-600 text-white px-4 py-4 sticky top-0 z-10 shadow-lg">
        <div className="max-w-lg mx-auto flex items-center gap-3">
          <Link to="/" className="p-2 hover:bg-purple-700 rounded-lg">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <div className="flex-1">
            <h1 className="text-xl font-bold">First Aid Quiz</h1>
            <p className="text-sm text-purple-200">
              Question {currentQuestion + 1} of {questions.length}
            </p>
          </div>
        </div>
      </header>

      <main className="max-w-lg mx-auto px-4 py-6 space-y-4">
        <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
          <div
            className="h-full bg-purple-600 transition-all"
            style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
          />
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg">
          <h2 className="text-lg font-bold text-gray-800 dark:text-gray-100 mb-6">
            {question.question}
          </h2>

          <div className="space-y-3">
            {question.options.map((option, index) => {
              const isSelected = selectedAnswer === index
              const isCorrectAnswer = index === question.correct

              return (
                <button
                  key={index}
                  onClick={() => handleAnswer(index)}
                  disabled={showResult}
                  className={`w-full p-4 rounded-xl text-left font-medium transition-all ${
                    showResult
                      ? isCorrectAnswer
                        ? 'bg-green-100 dark:bg-green-900/30 border-2 border-green-500 text-green-800 dark:text-green-200'
                        : isSelected
                        ? 'bg-red-100 dark:bg-red-900/30 border-2 border-red-500 text-red-800 dark:text-red-200'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400'
                      : isSelected
                      ? 'bg-purple-100 dark:bg-purple-900/30 border-2 border-purple-500 text-purple-800 dark:text-purple-200'
                      : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-100'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    {showResult && (isCorrectAnswer ? (
                      <Check className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0" />
                    ) : isSelected ? (
                      <X className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0" />
                    ) : (
                      <div className="w-5 h-5" />
                    ))}
                    <span>{option}</span>
                  </div>
                </button>
              )
            })}
          </div>
        </div>

        {showResult && (
          <div
            className={`rounded-xl p-4 border ${
              isCorrect
                ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
                : 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800'
            }`}
          >
            <div className="flex items-start gap-3">
              {isCorrect ? (
                <Check className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
              ) : (
                <X className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              )}
              <div>
                <h3 className={`font-medium ${isCorrect ? 'text-green-800 dark:text-green-200' : 'text-red-800 dark:text-red-200'}`}>
                  {isCorrect ? 'Correct!' : 'Incorrect'}
                </h3>
                <p className={`text-sm mt-1 ${isCorrect ? 'text-green-700 dark:text-green-300' : 'text-red-700 dark:text-red-300'}`}>
                  {question.explanation}
                </p>
              </div>
            </div>
          </div>
        )}

        {showResult && (
          <button
            onClick={handleNext}
            className="w-full py-4 bg-purple-600 hover:bg-purple-700 text-white rounded-xl font-medium transition-colors"
          >
            {currentQuestion < questions.length - 1 ? 'Next Question' : 'See Results'}
          </button>
        )}
      </main>
    </div>
  )
}
