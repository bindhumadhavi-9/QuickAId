import { useState, useRef, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft, Send, Bot, User, AlertTriangle, Phone, Flame, Droplets, Wind } from 'lucide-react'

interface Message {
  id: number
  sender: 'user' | 'bot'
  text: string
  timestamp: Date
}

const quickQuestions = [
  { icon: Droplets, label: 'How to stop bleeding?', question: 'How do I stop heavy bleeding?' },
  { icon: Flame, label: 'Treating burns', question: 'What is the proper way to treat a burn?' },
  { icon: Wind, label: 'Choking first aid', question: 'How do I help someone who is choking?' },
  { icon: Phone, label: 'When to call 911?', question: 'When should I call emergency services?' },
]

const aiResponses: Record<string, string> = {
  'how do i stop heavy bleeding?': `To stop heavy bleeding:

1. **Apply Direct Pressure** - Use a clean cloth or bandage and press firmly on the wound. Do not remove the cloth if it becomes soaked - add more on top.

2. **Elevate** - If possible, raise the injured area above the level of the heart.

3. **Apply Pressure Bandage** - Once bleeding slows, secure a pressure bandage over the wound.

4. **Seek Medical Help** - For deep wounds, wounds with embedded objects, or uncontrolled bleeding, seek immediate medical attention.

⚠️ **Warning**: Only use a tourniquet as a last resort for life-threatening bleeding that cannot be controlled by direct pressure.`,

  'what is the proper way to treat a burn?': `For burn treatment:

1. **Cool the Burn** - Run cool (not cold or ice) water over the burn for 10-20 minutes. Do not use ice, butter, or ointments.

2. **Remove Constrictions** - Remove jewelry, watches, or tight items from the burned area before swelling occurs.

3. **Cover the Burn** - Cover with a clean, non-stick bandage or plastic wrap. Do not break blisters.

4. **Relieve Pain** - Take over-the-counter pain relievers if needed.

⚠️ **Seek immediate medical care for**:
- Electrical or chemical burns
- Burns larger than 3 inches
- Burns on face, hands, feet, or genitals
- Third-degree burns (white/charred appearance)`,

  'how do i help someone who is choking?': `For a choking adult or child over 1 year:

**If they can still cough or speak**:
- Encourage them to continue coughing
- Do not interfere - let them try to dislodge it

**If they cannot breathe, cough, or speak**:
1. Stand behind them and wrap your arms around their waist
2. Make a fist with one hand and place it above their navel but below the ribs
3. Grasp your fist with your other hand
4. Give quick, upward abdominal thrusts (Heimlich maneuver)
5. Continue until the object is dislodged or they become unconscious

**If they become unconscious**:
- Lower them to the ground
- Begin CPR
- Call 911 immediately`,

  'when should i call emergency services?': `Call 911 or local emergency services for:

**Breathing Problems**:
- Difficulty breathing, choking, or stopping breathing

**Chest Pain**:
- Suspected heart attack, especially with sweating, nausea, or arm pain

**Unconsciousness**:
- Person who cannot be awakened or is unresponsive

**Severe Bleeding**:
- Blood that won't stop after 10-15 minutes of pressure
- Spurting blood

**Head/Neck/Back Injury**:
- Loss of consciousness, seizures, or clear fluid from ears/nose

**Severe Burns**:
- Electrical burns, chemical burns, or large/third-degree burns

**Stroke Signs**:
- Face drooping, arm weakness, speech difficulty

**Severe Allergic Reaction**:
- Difficulty breathing, swelling of throat/tongue

**When in doubt, call!** It's better to call and not need help than to wait when help is needed.`,

  'default': `I can help with common first aid questions. Here are some topics I can assist with:

- **Bleeding and wounds** - How to stop bleeding, clean cuts, and apply bandages
- **Burns** - Treatment for thermal, chemical, and electrical burns
- **Choking** - The Heimlich maneuver and CPR basics
- **Fractures** - How to immobilize suspected broken bones
- **Head injuries** - Recognizing concussion and when to seek help
- **Allergic reactions** - Recognizing and responding to anaphylaxis
- **CPR** - Basic CPR instructions for adults

Please select a quick question above or type your specific question. Remember - this is general guidance. Always seek professional medical help for serious emergencies!`,
}

export default function AIAssistant() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      sender: 'bot',
      text: "Hello! I'm your First Aid AI Assistant. I can provide general guidance on common first aid situations. How can I help you today?",
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = (question?: string) => {
    const text = question || input.trim()
    if (!text) return

    const userMessage: Message = {
      id: Date.now(),
      sender: 'user',
      text,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')

    setTimeout(() => {
      const lowerText = text.toLowerCase()
      let response = aiResponses.default

      for (const key of Object.keys(aiResponses)) {
        if (key !== 'default' && lowerText.includes(key.replace('?', ''))) {
          response = aiResponses[key]
          break
        }
      }

      const botMessage: Message = {
        id: Date.now() + 1,
        sender: 'bot',
        text: response,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, botMessage])
    }, 500)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col">
      <header className="bg-indigo-600 text-white px-4 py-4 sticky top-0 z-10 shadow-lg">
        <div className="max-w-lg mx-auto flex items-center gap-3">
          <Link to="/" className="p-2 hover:bg-indigo-700 rounded-lg">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <div className="flex items-center gap-2">
            <Bot className="w-6 h-6" />
            <h1 className="text-xl font-bold">AI First Aid Assistant</h1>
          </div>
        </div>
      </header>

      <div className="bg-amber-50 dark:bg-amber-900/20 border-b border-amber-200 dark:border-amber-800 px-4 py-2">
        <div className="max-w-lg mx-auto flex gap-2">
          <AlertTriangle className="w-4 h-4 text-amber-600 flex-shrink-0" />
          <p className="text-xs text-amber-700 dark:text-amber-300">
            This AI provides general guidance only. Always seek professional medical help for emergencies.
          </p>
        </div>
      </div>

      <main className="flex-1 max-w-lg w-full mx-auto px-4 py-4 overflow-y-auto">
        <div className="space-y-4">
          <div className="flex gap-2 flex-wrap">
            {quickQuestions.map((q) => (
              <button
                key={q.label}
                onClick={() => handleSend(q.question)}
                className="flex items-center gap-2 px-3 py-2 bg-white dark:bg-gray-800 rounded-lg text-sm font-medium hover:bg-gray-100 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-700 transition-colors"
              >
                <q.icon className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                {q.label}
              </button>
            ))}
          </div>

          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                  message.sender === 'user'
                    ? 'bg-indigo-600 text-white'
                    : 'bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 shadow-md'
                }`}
              >
                <div className="flex items-center gap-2 mb-1">
                  {message.sender === 'bot' ? (
                    <Bot className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                  ) : (
                    <User className="w-4 h-4" />
                  )}
                  <span className="text-xs opacity-70">
                    {message.sender === 'bot' ? 'AI Assistant' : 'You'}
                  </span>
                </div>
                <div className="prose prose-sm dark:prose-invert max-w-none">
                  {message.text.split('\n').map((line, i) => (
                    <p key={i} className="mb-1 last:mb-0 text-sm">
                      {line}
                    </p>
                  ))}
                </div>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </main>

      <div className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 px-4 py-3">
        <div className="max-w-lg mx-auto flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a first aid question..."
            className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
          <button
            onClick={() => handleSend()}
            disabled={!input.trim()}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  )
}
