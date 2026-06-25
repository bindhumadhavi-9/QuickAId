import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Phone, CheckCircle, AlertTriangle, ArrowRight, Volume2 } from 'lucide-react'
import { useState } from 'react'

const emergencyData: Record<string, {
  title: string
  icon: string
  warning: string
  steps: { step: number; title: string; description: string; critical?: boolean }[]
  callEmergency?: boolean
}> = {
  bleeding: {
    title: 'Bleeding Emergency',
    icon: 'Droplets',
    warning: 'For severe bleeding, apply direct pressure and call emergency services immediately.',
    steps: [
      { step: 1, title: 'Ensure Safety', description: 'Make sure the scene is safe before approaching. Put on protective gloves if available.' },
      { step: 2, title: 'Apply Direct Pressure', description: 'Use a clean cloth or bandage and apply firm, direct pressure to the wound. Do not remove the cloth if it becomes soaked - add more on top.', critical: true },
      { step: 3, title: 'Elevate the Injury', description: 'If possible, raise the injured area above the level of the heart to help reduce bleeding.' },
      { step: 4, title: 'Apply Pressure Bandage', description: 'Once bleeding slows, secure a pressure bandage over the wound. Do not apply a tourniquet unless trained to do so.' },
      { step: 5, title: 'Monitor for Shock', description: 'Watch for signs of shock: pale skin, rapid breathing, weak pulse. Keep the person warm and calm.' },
      { step: 6, title: 'Seek Medical Help', description: 'For deep wounds, wounds with embedded objects, or uncontrolled bleeding, seek immediate medical attention.', critical: true },
    ],
    callEmergency: true,
  },
  burns: {
    title: 'Burn Emergency',
    icon: 'Flame',
    warning: 'Severe burns require immediate medical attention. Do not apply ice, butter, or break blisters.',
    steps: [
      { step: 1, title: 'Stop the Burning', description: 'Remove the person from the heat source. Stop, drop, and roll if clothing is on fire.' },
      { step: 2, title: 'Cool the Burn', description: 'Run cool (not cold) water over the burn for 10-20 minutes. Do not use ice.', critical: true },
      { step: 3, title: 'Remove Constrictions', description: 'Remove jewelry, watches, or tight items from the burned area before swelling occurs.' },
      { step: 4, title: 'Cover the Burn', description: 'Cover with a clean, non-stick bandage or plastic wrap. Do not break blisters.' },
      { step: 5, title: 'Relieve Pain', description: 'Take over-the-counter pain relievers if needed. Avoid giving aspirin to children.' },
      { step: 6, title: 'Seek Medical Help', description: 'Seek immediate medical care for electrical burns, chemical burns, large burns, or burns on face/hands/genitals.', critical: true },
    ],
    callEmergency: true,
  },
  choking: {
    title: 'Choking Emergency',
    icon: 'Wind',
    warning: 'If the person cannot breathe, cough, or speak, begin the Heimlich maneuver immediately.',
    steps: [
      { step: 1, title: 'Assess the Situation', description: 'Ask "Are you choking?" If they can cough or speak, encourage them to continue coughing.' },
      { step: 2, title: 'Position Yourself', description: 'Stand behind the person. Wrap your arms around their waist.', critical: true },
      { step: 3, title: 'Perform Heimlich Maneuver', description: 'Make a fist with one hand. Place it above the navel but below the ribs. Grasp with your other hand and thrust upward and inward.', critical: true },
      { step: 4, title: 'Repeat Thrusts', description: 'Continue abdominal thrusts until the object is dislodged or the person becomes unconscious.' },
      { step: 5, title: 'If Person Becomes Unconscious', description: 'Lower them to the ground, begin CPR if trained, and call emergency services immediately.' },
      { step: 6, title: 'After Object is Removed', description: 'Seek medical attention to check for complications, even if breathing returns to normal.' },
    ],
    callEmergency: true,
  },
  fracture: {
    title: 'Fracture Emergency',
    icon: 'Bone',
    warning: 'Do not move the injured area unless absolutely necessary. Immobilization is critical.',
    steps: [
      { step: 1, title: 'Call Emergency Services', description: 'For obvious deformity, open fracture, or injury to head/neck/spine, do not move the person.', critical: true },
      { step: 2, title: 'Stop Any Bleeding', description: 'If there is an open wound with bleeding, apply pressure around the wound (not directly on protruding bone).' },
      { step: 3, title: 'Immobilize the Area', description: 'Do not attempt to realign the bone. Use splints (sticks, boards) to immobilize above and below the injury.' },
      { step: 4, title: 'Apply Ice', description: 'Apply ice wrapped in cloth to reduce swelling. Do not apply ice directly to skin.' },
      { step: 5, title: 'Elevate if Possible', description: 'If the limb can be elevated without causing pain, do so to reduce swelling.' },
      { step: 6, title: 'Monitor for Shock', description: 'Keep the person warm and calm. Watch for signs of shock: pale skin, rapid breathing, confusion.' },
    ],
    callEmergency: true,
  },
  'electric-shock': {
    title: 'Electric Shock Emergency',
    icon: 'Zap',
    warning: 'Do NOT touch the person if they are still in contact with the electrical source.',
    steps: [
      { step: 1, title: 'Do Not Touch the Person', description: 'If the person is still in contact with the electrical source, touching them can shock you too.', critical: true },
      { step: 2, title: 'Turn Off Power', description: 'Turn off the electricity at the main breaker or fuse box if possible.', critical: true },
      { step: 3, title: 'Separate from Source', description: 'If power cannot be turned off, use a non-conductive object (rubber, dry wood) to push the person away from the source.' },
      { step: 4, title: 'Call Emergency Services', description: 'Even if the person appears fine, they need medical evaluation. Internal injuries may not be visible.' },
      { step: 5, title: 'Check Breathing', description: 'If the person is not breathing, begin CPR if trained. Continue until help arrives.' },
      { step: 6, title: 'Treat Burns', description: 'Look for two burn sites (entry and exit wounds). Cover with clean bandages. Do not apply ice or ointments.' },
    ],
    callEmergency: true,
  },
  'head-injury': {
    title: 'Head Injury Emergency',
    icon: 'Brain',
    warning: 'Any head injury can be serious. Monitor for concussion symptoms and seek medical help.',
    steps: [
      { step: 1, title: 'Call Emergency Services', description: 'For loss of consciousness, severe headache, vomiting, seizures, or blood/fluid from ears/nose, call immediately.', critical: true },
      { step: 2, title: 'Keep Person Still', description: 'Do not move the person unless necessary. Keep their head and shoulders slightly elevated.' },
      { step: 3, title: 'Stop Any Bleeding', description: 'Apply gentle pressure to any bleeding wound with a clean cloth. Do not press if you suspect skull fracture.' },
      { step: 4, title: 'Monitor Breathing', description: 'Check breathing. If not breathing or no pulse, begin CPR if trained.' },
      { step: 5, title: 'Watch for Signs', description: 'Monitor for confusion, drowsiness, unequal pupils, weakness, or clear fluid from nose/ears. These indicate serious injury.' },
      { step: 6, title: 'Do Not Give Food/Drink', description: 'Avoid giving food or water in case surgery is needed. Keep the person calm and warm.' },
    ],
    callEmergency: true,
  },
  'heart-attack': {
    title: 'Heart Attack Emergency',
    icon: 'Heart',
    warning: 'Time is critical. Call emergency services immediately if you suspect a heart attack.',
    steps: [
      { step: 1, title: 'Call Emergency Services', description: 'Call immediately. Do not drive yourself to the hospital. Emergency responders can start treatment on the way.', critical: true },
      { step: 2, title: 'Keep Person Calm', description: 'Help the person sit in a comfortable position, slightly leaning back. Loosen tight clothing.' },
      { step: 3, title: 'Aspirin', description: 'If not allergic and emergency dispatcher approves, have the person chew (not swallow whole) one adult aspirin.' },
      { step: 4, title: 'Nitroglycerin', description: 'If prescribed nitroglycerin, help them take it as directed by their doctor.' },
      { step: 5, title: 'Begin CPR if Needed', description: 'If the person becomes unresponsive and is not breathing normally, begin CPR immediately and continue until help arrives.', critical: true },
      { step: 6, title: 'Use AED if Available', description: 'If an AED is available, turn it on and follow the voice prompts. Continue until emergency services arrive.' },
    ],
    callEmergency: true,
  },
  unconscious: {
    title: 'Unconscious Person',
    icon: 'Shield',
    warning: 'Check for breathing. If not breathing normally, begin CPR immediately.',
    steps: [
      { step: 1, title: 'Check for Danger', description: 'Ensure the scene is safe before approaching the person.' },
      { step: 2, title: 'Check Responsiveness', description: 'Tap their shoulder and ask loudly "Are you okay?" Check for breathing by looking, listening, and feeling for 10 seconds.' },
      { step: 3, title: 'Call Emergency Services', description: 'If unresponsive and not breathing normally, call emergency services and get an AED if available.', critical: true },
      { step: 4, title: 'Begin CPR', description: 'If not breathing normally, begin chest compressions: 30 compressions, then 2 rescue breaths. Continue until help arrives.', critical: true },
      { step: 5, title: 'Recovery Position', description: 'If breathing normally but unconscious, place in recovery position to maintain airway.' },
      { step: 6, title: 'Monitor Until Help Arrives', description: 'Check breathing regularly. Be prepared to begin CPR if breathing stops.' },
    ],
    callEmergency: true,
  },
}

export default function EmergencyWorkflow() {
  const { type } = useParams<{ type: string }>()
  const [currentStep, setCurrentStep] = useState(0)
  const emergency = emergencyData[type || '']

  if (!emergency) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-500 dark:text-gray-400">Emergency type not found</p>
          <Link to="/emergency" className="text-red-600 hover:underline mt-2 inline-block">
            Back to emergencies
          </Link>
        </div>
      </div>
    )
  }

  const handleSpeak = (text: string) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.rate = 0.9
      speechSynthesis.speak(utterance)
    }
  }

  const totalSteps = emergency.steps.length
  const progress = ((currentStep + 1) / totalSteps) * 100

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <header className="bg-red-600 text-white px-4 py-4 sticky top-0 z-10 shadow-lg">
        <div className="max-w-lg mx-auto flex items-center gap-3">
          <Link to="/emergency" className="p-2 hover:bg-red-700 rounded-lg">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <h1 className="text-lg font-bold">{emergency.title}</h1>
        </div>
      </header>

      <main className="max-w-lg mx-auto px-4 py-6 space-y-4">
        {emergency.callEmergency && (
          <button
            onClick={() => window.location.href = 'tel:911'}
            className="w-full bg-red-600 hover:bg-red-700 text-white rounded-xl p-4 flex items-center justify-center gap-3 shadow-lg sos-pulse"
          >
            <Phone className="w-6 h-6" />
            <span className="font-bold">Call 911 Now</span>
          </button>
        )}

        <div className="bg-amber-50 dark:bg-amber-900/20 rounded-xl p-4 border border-amber-200 dark:border-amber-800">
          <div className="flex gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-amber-700 dark:text-amber-300">{emergency.warning}</p>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
          <div className="h-2 bg-gray-200 dark:bg-gray-700">
            <div
              className="h-full bg-green-600 transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>

          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm text-gray-500 dark:text-gray-400">
                Step {currentStep + 1} of {totalSteps}
              </span>
              <button
                onClick={() => handleSpeak(`${emergency.steps[currentStep].title}. ${emergency.steps[currentStep].description}`)}
                className="flex items-center gap-1 text-blue-600 dark:text-blue-400 text-sm hover:underline"
              >
                <Volume2 className="w-4 h-4" />
                Read aloud
              </button>
            </div>

            <div
              className={`p-4 rounded-xl ${
                emergency.steps[currentStep].critical
                  ? 'bg-red-50 dark:bg-red-900/20 border-2 border-red-300 dark:border-red-700'
                  : 'bg-gray-50 dark:bg-gray-700/50'
              }`}
            >
              <div className="flex items-start gap-3">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    emergency.steps[currentStep].critical
                      ? 'bg-red-600 text-white'
                      : 'bg-green-600 text-white'
                  }`}
                >
                  {emergency.steps[currentStep].step}
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-gray-800 dark:text-gray-100 mb-2">
                    {emergency.steps[currentStep].title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                    {emergency.steps[currentStep].description}
                  </p>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between mt-6 gap-3">
              <button
                onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
                disabled={currentStep === 0}
                className="flex-1 py-3 px-4 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              >
                Previous
              </button>

              {currentStep < totalSteps - 1 ? (
                <button
                  onClick={() => setCurrentStep(currentStep + 1)}
                  className="flex-1 py-3 px-4 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 transition-colors flex items-center justify-center gap-2"
                >
                  Next Step
                  <ArrowRight className="w-4 h-4" />
                </button>
              ) : (
                <Link
                  to="/"
                  className="flex-1 py-3 px-4 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 transition-colors flex items-center justify-center gap-2"
                >
                  <CheckCircle className="w-4 h-4" />
                  Complete
                </Link>
              )}
            </div>
          </div>
        </div>

        <div className="flex gap-2 flex-wrap">
          {emergency.steps.map((_, idx) => (
            <button
              key={idx}
              onClick={() => setCurrentStep(idx)}
              className={`w-10 h-10 rounded-lg font-medium transition-colors ${
                idx === currentStep
                  ? 'bg-green-600 text-white'
                  : idx < currentStep
                  ? 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400'
              }`}
            >
              {idx + 1}
            </button>
          ))}
        </div>
      </main>
    </div>
  )
}
