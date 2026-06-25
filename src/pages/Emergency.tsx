import { Link } from 'react-router-dom'
import { ArrowLeft, Phone, Droplets, Flame, Wind, Zap, Shield, AlertTriangle, Heart, Bone, Brain } from 'lucide-react'

const emergencies = [
  { type: 'bleeding', icon: Droplets, label: 'Bleeding', color: 'text-red-600 bg-red-100 dark:bg-red-900/30', desc: 'Cuts, wounds, heavy bleeding' },
  { type: 'burns', icon: Flame, label: 'Burns', color: 'text-orange-600 bg-orange-100 dark:bg-orange-900/30', desc: 'Thermal, chemical, electrical burns' },
  { type: 'choking', icon: Wind, label: 'Choking', color: 'text-purple-600 bg-purple-100 dark:bg-purple-900/30', desc: 'Airway obstruction' },
  { type: 'fracture', icon: Bone, label: 'Fracture', color: 'text-blue-600 bg-blue-100 dark:bg-blue-900/30', desc: 'Broken bones, sprains' },
  { type: 'electric-shock', icon: Zap, label: 'Electric Shock', color: 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30', desc: 'Electrical injury response' },
  { type: 'head-injury', icon: Brain, label: 'Head Injury', color: 'text-pink-600 bg-pink-100 dark:bg-pink-900/30', desc: 'Concussion, head trauma' },
  { type: 'heart-attack', icon: Heart, label: 'Heart Attack', color: 'text-red-600 bg-red-100 dark:bg-red-900/30', desc: 'Cardiac emergency' },
  { type: 'unconscious', icon: Shield, label: 'Unconscious Person', color: 'text-gray-600 bg-gray-100 dark:bg-gray-900/30', desc: 'Fainting, unconsciousness' },
]

export default function Emergency() {
  const handleSOS = () => {
    window.location.href = 'tel:911'
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <header className="bg-red-600 text-white px-4 py-4 sticky top-0 z-10 shadow-lg">
        <div className="max-w-lg mx-auto flex items-center gap-3">
          <Link to="/" className="p-2 hover:bg-red-700 rounded-lg">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <h1 className="text-xl font-bold">Emergency Response</h1>
        </div>
      </header>

      <main className="max-w-lg mx-auto px-4 py-6 space-y-6">
        <button
          onClick={handleSOS}
          className="w-full bg-red-600 hover:bg-red-700 text-white rounded-2xl p-6 text-center shadow-lg sos-pulse transition-all"
        >
          <Phone className="w-14 h-14 mx-auto mb-2" />
          <span className="text-xl font-bold">SOS - Call 911</span>
          <p className="text-red-100 text-sm mt-1">Immediate emergency assistance</p>
        </button>

        <div className="bg-amber-50 dark:bg-amber-900/20 rounded-xl p-4 border border-amber-200 dark:border-amber-800">
          <div className="flex gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-amber-700 dark:text-amber-300">
              Select the type of emergency for step-by-step first aid guidance. Call emergency services first!
            </p>
          </div>
        </div>

        <section>
          <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-3">Select Emergency Type</h2>
          <div className="grid grid-cols-2 gap-3">
            {emergencies.map((emergency) => (
              <Link
                key={emergency.type}
                to={`/emergency/${emergency.type}`}
                className="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-md hover:shadow-lg transition-all border border-gray-100 dark:border-gray-700"
              >
                <div className={`w-12 h-12 rounded-full ${emergency.color} flex items-center justify-center mb-3`}>
                  <emergency.icon className="w-6 h-6" />
                </div>
                <h3 className="font-medium text-gray-800 dark:text-gray-100">{emergency.label}</h3>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{emergency.desc}</p>
              </Link>
            ))}
          </div>
        </section>
      </main>
    </div>
  )
}
