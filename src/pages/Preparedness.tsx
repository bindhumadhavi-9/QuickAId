import { Link, useParams } from 'react-router-dom'
import { ArrowLeft, Shield, Waves, Flame, Wind, Zap, Snowflake, Mountain, ArrowRight, AlertTriangle, CheckCircle } from 'lucide-react'

const disasterTypes: Record<string, {
  icon: typeof Shield
  title: string
  description: string
  color: string
  before: string[]
  during: string[]
  after: string[]
}> = {
  earthquake: {
    icon: Mountain,
    title: 'Earthquake Safety',
    description: 'Be prepared for seismic activity with proper response techniques',
    color: 'bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400',
    before: [
      'Secure heavy furniture and appliances to walls',
      'Create an emergency kit with food, water, and supplies',
      'Plan and practice earthquake drills with family',
      'Identify safe spots in each room (under sturdy furniture, against interior walls)',
      'Know how to shut off gas, water, and electricity',
    ],
    during: [
      'DROP to hands and knees',
      'Take COVER under sturdy furniture or against interior wall',
      'HOLD ON until shaking stops',
      'Stay away from windows, exterior walls, and heavy objects',
      'If outdoors, move away from buildings, trees, and power lines',
    ],
    after: [
      'Check yourself and others for injuries',
      'Expect aftershocks and be ready to drop, cover, and hold on',
      'Check for damage to your building and evacuate if unsafe',
      'Listen to emergency broadcasts for information',
      'Be careful when cleaning up - wear protective clothing',
    ],
  },
  flood: {
    icon: Waves,
    title: 'Flood Safety',
    description: 'Know how to prepare and respond to flooding emergencies',
    color: 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400',
    before: [
      'Know your area\'s flood risk and evacuation routes',
      'Elevate appliances and utilities if possible',
      'Install check valves in plumbing to prevent backup',
      'Have emergency supplies ready in waterproof containers',
      'Never ignore evacuation orders',
    ],
    during: [
      'Move to higher ground immediately',
      'Never walk, swim, or drive through flood waters',
      'Just 6 inches of moving water can knock you down',
      'If trapped in a vehicle, abandon it and move to higher ground',
      'Stay off bridges over fast-moving water',
    ],
    after: [
      'Avoid flood water - may contain sewage, chemicals, or sharp debris',
      'Do not drink tap water until declared safe',
      'Document damage for insurance before cleaning',
      'Wear protective gear during cleanup',
      'Be aware of electrical hazards - do not touch wet electrical equipment',
    ],
  },
  fire: {
    icon: Flame,
    title: 'Fire Safety',
    description: 'Prevent fires and know how to respond if one occurs',
    color: 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400',
    before: [
      'Install smoke detectors on every level and test monthly',
      'Create a fire escape plan with two exits per room',
      'Practice fire drills with your family',
      'Keep fire extinguishers and know how to use them',
      'Clear flammable materials from around your home',
    ],
    during: [
      'Get out, stay out, call for help',
      'Crawl low under smoke to breathe cleaner air',
      'Feel doors before opening - if hot, use alternate exit',
      'Close doors behind you to slow fire spread',
      'Never use elevators during a fire',
      'If clothes catch fire: STOP, DROP, and ROLL',
    ],
    after: [
      'Do not re-enter until cleared by fire department',
      'Contact your insurance company',
      'Document damage with photos and videos',
      'Check for hidden hazards like smoldering materials',
      'Seek medical attention if you inhaled smoke',
    ],
  },
  cyclone: {
    icon: Wind,
    title: 'Cyclone/Hurricane Safety',
    description: 'Prepare for high winds and severe storms',
    color: 'bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400',
    before: [
      'Know your evacuation zone and routes',
      'Stock emergency supplies for at least 3 days',
      'Reinforce windows or install storm shutters',
      'Secure or bring inside outdoor furniture and objects',
      'Fill bathtubs with water for cleaning (not drinking)',
    ],
    during: [
      'Stay indoors away from windows and glass doors',
      'Go to a small interior room on the lowest floor',
      'Do not go outside during the eye - winds will return',
      'Monitor emergency broadcasts',
      'If flooding occurs, move to higher ground',
    ],
    after: [
      'Wait for official all-clear before going outside',
      'Avoid flood waters and downed power lines',
      'Check for structural damage before entering buildings',
      'Use flashlights - not candles - to check for damage',
      'Document damage for insurance',
    ],
  },
  lightning: {
    icon: Zap,
    title: 'Lightning Safety',
    description: 'Stay safe during thunderstorms',
    color: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-600 dark:text-yellow-400',
    before: [
      'Postpone outdoor activities if thunderstorms predicted',
      'Check weather forecasts before outdoor activities',
      'Know the 30-30 rule: seek shelter if flash to bang is 30 seconds or less',
      'Have emergency supplies ready',
    ],
    during: [
      'Seek shelter in a sturdy building or hard-top vehicle',
      'Avoid windows, doors, and porches',
      'Do not use corded phones or electrical equipment',
      'Stay away from water - showers, baths, sinks',
      'If outdoors with no shelter: avoid tall trees, water, and metal objects',
    ],
    after: [
      'Wait 30 minutes after the last thunder before going outside',
      'Help anyone struck by lightning - they do not carry a charge',
      'Check for injuries, give CPR if needed',
      'Report downed power lines',
    ],
  },
  winter: {
    icon: Snowflake,
    title: 'Winter Storm Safety',
    description: 'Prepare for severe cold, snow, and ice',
    color: 'bg-cyan-100 dark:bg-cyan-900/30 text-cyan-600 dark:text-cyan-400',
    before: [
      'Winterize your home and vehicle',
      'Stock emergency supplies including warm clothing and blankets',
      'Insulate pipes and allow faucets to drip during cold snaps',
      'Have alternative heating sources ready',
      'Keep vehicle gas tank full for emergencies',
    ],
    during: [
      'Stay indoors as much as possible',
      'Dress in warm layers if you must go outside',
      'Conserve heat by closing unused rooms',
      'Watch for signs of hypothermia and frostbite',
      'Never use generators or grills indoors',
    ],
    after: [
      'Check on neighbors, especially elderly or disabled',
      'Watch for ice dams and roof damage from snow weight',
      'Clear walkways carefully to avoid injury',
      'Allow faucets to drip slowly to prevent frozen pipes',
      'Warm up gradually - hot drinks, warm (not hot) water',
    ],
  },
}

export default function Preparedness() {
  const { topic } = useParams<{ topic: string }>()

  if (topic && disasterTypes[topic]) {
    const disaster = disasterTypes[topic]
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <header className="bg-green-600 text-white px-4 py-4 sticky top-0 z-10 shadow-lg">
          <div className="max-w-lg mx-auto flex items-center gap-3">
            <Link to="/preparedness" className="p-2 hover:bg-green-700 rounded-lg">
              <ArrowLeft className="w-6 h-6" />
            </Link>
            <h1 className="text-xl font-bold">{disaster.title}</h1>
          </div>
        </header>

        <main className="max-w-lg mx-auto px-4 py-6 space-y-6">
          <div className={`rounded-2xl p-6 ${disaster.color}`}>
            <disaster.icon className="w-12 h-12 mx-auto mb-3" />
            <p className="text-center text-sm">{disaster.description}</p>
          </div>

          <section>
            <h2 className="text-lg font-bold text-gray-800 dark:text-gray-100 flex items-center gap-2 mb-3">
              <CheckCircle className="w-5 h-5 text-green-600" />
              Before
            </h2>
            <div className="space-y-2">
              {disaster.before.map((item, idx) => (
                <div key={idx} className="bg-white dark:bg-gray-800 rounded-lg p-3 shadow-sm border border-gray-100 dark:border-gray-700">
                  <p className="text-sm text-gray-700 dark:text-gray-300">{item}</p>
                </div>
              ))}
            </div>
          </section>

          <section>
            <h2 className="text-lg font-bold text-gray-800 dark:text-gray-100 flex items-center gap-2 mb-3">
              <AlertTriangle className="w-5 h-5 text-amber-600" />
              During
            </h2>
            <div className="space-y-2">
              {disaster.during.map((item, idx) => (
                <div key={idx} className="bg-amber-50 dark:bg-amber-900/20 rounded-lg p-3 border border-amber-200 dark:border-amber-800">
                  <p className="text-sm text-amber-800 dark:text-amber-200">{item}</p>
                </div>
              ))}
            </div>
          </section>

          <section>
            <h2 className="text-lg font-bold text-gray-800 dark:text-gray-100 flex items-center gap-2 mb-3">
              <ArrowRight className="w-5 h-5 text-blue-600" />
              After
            </h2>
            <div className="space-y-2">
              {disaster.after.map((item, idx) => (
                <div key={idx} className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3 border border-blue-200 dark:border-blue-800">
                  <p className="text-sm text-blue-800 dark:text-blue-200">{item}</p>
                </div>
              ))}
            </div>
          </section>
        </main>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <header className="bg-green-600 text-white px-4 py-4 sticky top-0 z-10 shadow-lg">
        <div className="max-w-lg mx-auto flex items-center gap-3">
          <Link to="/" className="p-2 hover:bg-green-700 rounded-lg">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <h1 className="text-xl font-bold">Disaster Preparedness</h1>
        </div>
      </header>

      <main className="max-w-lg mx-auto px-4 py-6 space-y-6">
        <div className="bg-green-50 dark:bg-green-900/20 rounded-xl p-4 border border-green-200 dark:border-green-800">
          <p className="text-sm text-green-700 dark:text-green-300">
            Being prepared can save lives. Learn how to prepare for, respond to, and recover from various disasters.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-3">
          {Object.entries(disasterTypes).map(([key, disaster]) => (
            <Link
              key={key}
              to={`/preparedness/${key}`}
              className="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-md hover:shadow-lg transition-all border border-gray-100 dark:border-gray-700 flex flex-col items-center text-center gap-2"
            >
              <div className={`w-12 h-12 rounded-full ${disaster.color} flex items-center justify-center`}>
                <disaster.icon className="w-6 h-6" />
              </div>
              <h3 className="font-medium text-gray-800 dark:text-gray-100 text-sm">{disaster.title.replace(' Safety', '')}</h3>
            </Link>
          ))}
        </div>
      </main>
    </div>
  )
}
