import { Link } from 'react-router-dom'
import {
  Phone,
  Users,
  Accessibility,
  Briefcase,
  Brain,
  Shield,
  AlertTriangle,
  BookOpen,
} from 'lucide-react'

export default function Home() {
  const quickActions = [
    { to: '/emergency', icon: AlertTriangle, label: 'SOS Emergency', color: 'bg-red-600', urgent: true },
    { to: '/body-map', icon: Accessibility, label: 'Body Map', color: 'bg-blue-600' },
    { to: '/contacts', icon: Users, label: 'Emergency Contacts', color: 'bg-green-600' },
    { to: '/first-aid-kit', icon: Briefcase, label: 'First Aid Kit', color: 'bg-amber-600' },
  ]

  const features = [
    { to: '/preparedness', icon: Shield, label: 'Disaster Prep', desc: 'Earthquake, Flood, Fire safety' },
    { to: '/quiz', icon: Brain, label: 'Practice Quiz', desc: 'Test your first aid knowledge' },
    { to: '/ai-assistant', icon: BookOpen, label: 'AI Assistant', desc: 'Get instant guidance' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-red-50 to-white dark:from-gray-900 dark:to-gray-800">
      <header className="bg-red-600 text-white px-4 py-6 shadow-lg">
        <div className="max-w-lg mx-auto">
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <Shield className="w-8 h-8" />
            QuickAid
          </h1>
          <p className="text-red-100 text-sm mt-1">Emergency First Aid Assistant</p>
        </div>
      </header>

      <main className="max-w-lg mx-auto px-4 py-6 space-y-6">
        <Link
          to="/emergency"
          className="block bg-red-600 hover:bg-red-700 text-white rounded-2xl p-6 text-center shadow-lg sos-pulse transition-all"
        >
          <Phone className="w-16 h-16 mx-auto mb-3" />
          <span className="text-2xl font-bold">SOS - Call Emergency</span>
          <p className="text-red-100 text-sm mt-2">Tap to call local emergency services</p>
        </Link>

        <section>
          <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-3">Quick Actions</h2>
          <div className="grid grid-cols-2 gap-3">
            {quickActions.slice(1).map((action) => (
              <Link
                key={action.to}
                to={action.to}
                className={`${action.color} hover:opacity-90 text-white rounded-xl p-4 flex flex-col items-center gap-2 transition-all shadow-md`}
              >
                <action.icon className="w-8 h-8" />
                <span className="text-sm font-medium text-center">{action.label}</span>
              </Link>
            ))}
          </div>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-3">Learn & Prepare</h2>
          <div className="space-y-3">
            {features.map((feature) => (
              <Link
                key={feature.to}
                to={feature.to}
                className="flex items-center gap-4 bg-white dark:bg-gray-800 rounded-xl p-4 shadow-md hover:shadow-lg transition-all border border-gray-100 dark:border-gray-700"
              >
                <div className="w-12 h-12 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
                  <feature.icon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                </div>
                <div>
                  <h3 className="font-medium text-gray-800 dark:text-gray-100">{feature.label}</h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">{feature.desc}</p>
                </div>
              </Link>
            ))}
          </div>
        </section>

        <section className="bg-amber-50 dark:bg-amber-900/20 rounded-xl p-4 border border-amber-200 dark:border-amber-800">
          <div className="flex gap-3">
            <AlertTriangle className="w-6 h-6 text-amber-600 flex-shrink-0" />
            <div>
              <h3 className="font-medium text-amber-800 dark:text-amber-200">Disclaimer</h3>
              <p className="text-sm text-amber-700 dark:text-amber-300 mt-1">
                This app provides general first aid guidance. Always seek professional medical help in emergencies.
              </p>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}


export default Home