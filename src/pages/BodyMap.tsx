import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft, Info, AlertTriangle, X } from 'lucide-react'

const bodyParts: Record<string, {
  name: string
  info: string
  commonIssues: { name: string; treatment: string }[]
  warning?: string
  emergencyLink?: string
}> = {
  head: {
    name: 'Head & Brain',
    info: 'Head injuries can be serious. Always monitor for concussion symptoms.',
    commonIssues: [
      { name: 'Concussion', treatment: 'Rest in a quiet, dark room. Monitor for worsening symptoms. Seek medical help if vomiting, confusion, or drowsiness occurs.' },
      { name: 'Scalp Wound', treatment: 'Apply gentle pressure with a clean cloth. Seek medical help for deep cuts or if bleeding won\'t stop after 10-15 minutes.' },
      { name: 'Headache', treatment: 'Rest in a quiet space. Apply cool compress. Stay hydrated. Seek help for sudden severe headaches or headaches after injury.' },
    ],
    warning: 'Call emergency services for loss of consciousness, seizures, clear fluid from ears/nose, or unequal pupils.',
    emergencyLink: '/emergency/head-injury',
  },
  face: {
    name: 'Face',
    info: 'Facial injuries can affect breathing and eating. Watch for signs of fractures.',
    commonIssues: [
      { name: 'Nosebleed', treatment: 'Sit leaning forward. Pinch the soft part of nostrils for 10-15 minutes. Apply ice to bridge of nose. Do not tilt head back.' },
      { name: 'Black Eye', treatment: 'Apply cold compress for 15-20 minutes. Do not press on the eye. Seek help if vision changes or double vision.' },
      { name: 'Lip Wound', treatment: 'Clean with water. Apply pressure for minor cuts. Seek help for deep cuts through the lip border.' },
    ],
  },
  eye: {
    name: 'Eye',
    info: 'Eye injuries require careful handling. Do not rub or apply pressure.',
    commonIssues: [
      { name: 'Foreign Object', treatment: 'Do not rub. Try to flush with clean water or saline. If object is embedded, do not remove - seek medical help.' },
      { name: 'Chemical Exposure', treatment: 'Flush immediately with clean water for at least 15-20 minutes. Remove contacts. Seek emergency care immediately.' },
      { name: 'Black Eye / Trauma', treatment: 'Apply cold compress. Do not apply pressure. Seek help for vision changes, severe pain, or visible damage.' },
    ],
    warning: 'Chemical exposure requires immediate flushing. Never apply pressure to the eye.',
    emergencyLink: '/emergency/head-injury',
  },
  neck: {
    name: 'Neck & Spine',
    info: 'Neck and spine injuries can cause paralysis. Keep the person still.',
    commonIssues: [
      { name: 'Neck Strain', treatment: 'Apply ice for first 24 hours, then heat. Gentle movement. Seek help if pain persists or numbness occurs.' },
      { name: 'Whiplash', treatment: 'Apply cold compress. Rest. Gradual gentle movement. Seek medical evaluation.' },
      { name: 'Suspected Spine Injury', treatment: 'DO NOT move the person. Keep head and neck stable. Call emergency services immediately.' },
    ],
    warning: 'If spine injury is suspected, DO NOT move the person. Call emergency services.',
  },
  chest: {
    name: 'Chest & Heart',
    info: 'Chest pain can indicate serious conditions. Always treat as potential emergency.',
    commonIssues: [
      { name: 'Suspected Heart Attack', treatment: 'Call emergency services. Keep person calm and seated. Chew aspirin if not allergic. Begin CPR if unresponsive.' },
      { name: 'Rib Injury', treatment: 'Apply ice. Take shallow breaths. Seek medical help for difficulty breathing or severe pain.' },
      { name: 'Chest Wound', treatment: 'Apply pressure with clean cloth. For penetrating wounds, do not remove object. Seek immediate medical help.' },
    ],
    warning: 'Any chest pain should be evaluated by medical professionals.',
    emergencyLink: '/emergency/heart-attack',
  },
  abdomen: {
    name: 'Abdomen',
    info: 'Abdominal injuries can cause internal bleeding. External wounds may look minor but be serious.',
    commonIssues: [
      { name: 'Blunt Trauma', treatment: 'Watch for pain, swelling, bruising. Seek medical help if pain worsens, vomit, or blood in urine/stool.' },
      { name: 'Penetrating Wound', treatment: 'DO NOT remove object. Stabilize it. Call emergency services. Apply gentle pressure around wound.' },
      { name: 'Stomach Pain', treatment: 'Rest. Avoid food. Seek help for severe pain, fever, bloody stool, or persistent vomiting.' },
    ],
    warning: 'Internal injuries may not show symptoms immediately. Seek medical evaluation after significant trauma.',
  },
  arm_left: {
    name: 'Left Arm',
    info: 'Arm injuries are common. Watch for fractures and circulation issues.',
    commonIssues: [
      { name: 'Fracture', treatment: 'Immobilize with splint. Apply ice. Do not try to realign. Seek medical help.' },
      { name: 'Cut/Laceration', treatment: 'Apply direct pressure. Elevate arm. Clean and bandage when bleeding stops.' },
      { name: 'Sprain', treatment: 'RICE: Rest, Ice, Compression, Elevation. Seek help if unable to move or bear weight.' },
    ],
    emergencyLink: '/emergency/fracture',
  },
  arm_right: {
    name: 'Right Arm',
    info: 'Arm injuries are common. Watch for fractures and circulation issues.',
    commonIssues: [
      { name: 'Fracture', treatment: 'Immobilize with splint. Apply ice. Do not try to realign. Seek medical help.' },
      { name: 'Cut/Laceration', treatment: 'Apply direct pressure. Elevate arm. Clean and bandage when bleeding stops.' },
      { name: 'Sprain', treatment: 'RICE: Rest, Ice, Compression, Elevation. Seek help if unable to move or bear weight.' },
    ],
    emergencyLink: '/emergency/fracture',
  },
  hand_left: {
    name: 'Left Hand',
    info: 'Hand injuries affect fine motor skills. Watch for circulation and nerve damage.',
    commonIssues: [
      { name: 'Finger Cut', treatment: 'Apply pressure. For fingertip amputation, wrap part in clean cloth, place in bag, keep cool (not frozen).' },
      { name: 'Burn', treatment: 'Cool under running water for 10-20 minutes. Cover with clean bandage. Seek help for large or deep burns.' },
      { name: 'Fracture', treatment: 'Immobilize finger. Apply ice. Seek medical help to ensure proper healing.' },
    ],
    emergencyLink: '/emergency/bleeding',
  },
  hand_right: {
    name: 'Right Hand',
    info: 'Hand injuries affect fine motor skills. Watch for circulation and nerve damage.',
    commonIssues: [
      { name: 'Finger Cut', treatment: 'Apply pressure. For fingertip amputation, wrap part in clean cloth, place in bag, keep cool (not frozen).' },
      { name: 'Burn', treatment: 'Cool under running water for 10-20 minutes. Cover with clean bandage. Seek help for large or deep burns.' },
      { name: 'Fracture', treatment: 'Immobilize finger. Apply ice. Seek medical help to ensure proper healing.' },
    ],
    emergencyLink: '/emergency/bleeding',
  },
  leg_left: {
    name: 'Left Leg',
    info: 'Leg injuries can affect mobility. Immobilize and seek help for suspected fractures.',
    commonIssues: [
      { name: 'Fracture', treatment: 'Do not move. Immobilize with splint or by binding to other leg. Call for help.' },
      { name: 'Deep Wound', treatment: 'Apply direct pressure. Elevate leg if possible. Seek help for uncontrolled bleeding.' },
      { name: 'Sprain/Strain', treatment: 'RICE: Rest, Ice, Compression, Elevation. Avoid putting weight on it.' },
    ],
    emergencyLink: '/emergency/fracture',
  },
  leg_right: {
    name: 'Right Leg',
    info: 'Leg injuries can affect mobility. Immobilize and seek help for suspected fractures.',
    commonIssues: [
      { name: 'Fracture', treatment: 'Do not move. Immobilize with splint or by binding to other leg. Call for help.' },
      { name: 'Deep Wound', treatment: 'Apply direct pressure. Elevate leg if possible. Seek help for uncontrolled bleeding.' },
      { name: 'Sprain/Strain', treatment: 'RICE: Rest, Ice, Compression, Elevation. Avoid putting weight on it.' },
    ],
    emergencyLink: '/emergency/fracture',
  },
  foot_left: {
    name: 'Left Foot',
    info: 'Foot injuries affect walking. Check for proper circulation.',
    commonIssues: [
      { name: 'Ankle Sprain', treatment: 'RICE: Rest, Ice, Compression, Elevation. Avoid walking. Seek help if unable to bear weight.' },
      { name: 'Toe Injury', treatment: 'Buddy tape injured toe to adjacent toe. Apply ice. Seek help if severely deformed.' },
      { name: 'Puncture Wound', treatment: 'Clean thoroughly. Apply antibiotic. Watch for infection signs. Tetanus shot may be needed.' },
    ],
  },
  foot_right: {
    name: 'Right Foot',
    info: 'Foot injuries affect walking. Check for proper circulation.',
    commonIssues: [
      { name: 'Ankle Sprain', treatment: 'RICE: Rest, Ice, Compression, Elevation. Avoid walking. Seek help if unable to bear weight.' },
      { name: 'Toe Injury', treatment: 'Buddy tape injured toe to adjacent toe. Apply ice. Seek help if severely deformed.' },
      { name: 'Puncture Wound', treatment: 'Clean thoroughly. Apply antibiotic. Watch for infection signs. Tetanus shot may be needed.' },
    ],
  },
}

export default function BodyMap() {
  const [selectedPart, setSelectedPart] = useState<string | null>(null)

  const bodyPart = selectedPart ? bodyParts[selectedPart] : null

  const getPartColor = (partId: string) => {
    if (selectedPart === partId) return '#22c55e'
    if (selectedPart) return '#94a3b8'
    return '#3b82f6'
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <header className="bg-blue-600 text-white px-4 py-4 sticky top-0 z-10 shadow-lg">
        <div className="max-w-lg mx-auto flex items-center gap-3">
          <Link to="/" className="p-2 hover:bg-blue-700 rounded-lg">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <h1 className="text-xl font-bold">Interactive Body Map</h1>
        </div>
      </header>

      <main className="max-w-lg mx-auto px-4 py-6 space-y-4">
        <p className="text-center text-gray-600 dark:text-gray-400">
          Tap on a body part to see first aid guidance
        </p>

        <div className="bg-white dark:bg-gray-800 rounded-2xl p-4 shadow-lg">
          <svg
            viewBox="0 0 200 400"
            className="w-full max-w-xs mx-auto"
            style={{ minHeight: '300px' }}
          >
            <ellipse cx="100" cy="35" rx="25" ry="30" fill={getPartColor('head')} onClick={() => setSelectedPart(selectedPart === 'head' ? null : 'head')} className="cursor-pointer hover:opacity-80 transition-all" />
            <ellipse cx="55" cy="35" rx="8" ry="6" fill={getPartColor('eye')} onClick={() => setSelectedPart(selectedPart === 'eye' ? null : 'eye')} className="cursor-pointer hover:opacity-80 transition-all" />
            <ellipse cx="145" cy="35" rx="8" ry="6" fill={getPartColor('eye')} onClick={() => setSelectedPart(selectedPart === 'eye' ? null : 'eye')} className="cursor-pointer hover:opacity-80 transition-all" />
            <ellipse cx="100" cy="30" rx="15" ry="10" fill={getPartColor('face')} onClick={() => setSelectedPart(selectedPart === 'face' ? null : 'face')} className="cursor-pointer hover:opacity-80 transition-all opacity-0" style={{ opacity: 0.5 }} />
            <rect x="85" y="65" width="30" height="35" rx="10" fill={getPartColor('neck')} onClick={() => setSelectedPart(selectedPart === 'neck' ? null : 'neck')} className="cursor-pointer hover:opacity-80 transition-all" />
            <ellipse cx="100" cy="130" rx="35" ry="40" fill={getPartColor('chest')} onClick={() => setSelectedPart(selectedPart === 'chest' ? null : 'chest')} className="cursor-pointer hover:opacity-80 transition-all" />
            <ellipse cx="100" cy="190" rx="30" ry="30" fill={getPartColor('abdomen')} onClick={() => setSelectedPart(selectedPart === 'abdomen' ? null : 'abdomen')} className="cursor-pointer hover:opacity-80 transition-all" />
            <rect x="40" y="100" width="20" height="70" rx="10" fill={getPartColor('arm_left')} onClick={() => setSelectedPart(selectedPart === 'arm_left' ? null : 'arm_left')} className="cursor-pointer hover:opacity-80 transition-all" />
            <rect x="140" y="100" width="20" height="70" rx="10" fill={getPartColor('arm_right')} onClick={() => setSelectedPart(selectedPart === 'arm_right' ? null : 'arm_right')} className="cursor-pointer hover:opacity-80 transition-all" />
            <ellipse cx="45" cy="180" rx="15" ry="12" fill={getPartColor('hand_left')} onClick={() => setSelectedPart(selectedPart === 'hand_left' ? null : 'hand_left')} className="cursor-pointer hover:opacity-80 transition-all" />
            <ellipse cx="155" cy="180" rx="15" ry="12" fill={getPartColor('hand_right')} onClick={() => setSelectedPart(selectedPart === 'hand_right' ? null : 'hand_right')} className="cursor-pointer hover:opacity-80 transition-all" />
            <rect x="70" y="220" width="25" height="100" rx="12" fill={getPartColor('leg_left')} onClick={() => setSelectedPart(selectedPart === 'leg_left' ? null : 'leg_left')} className="cursor-pointer hover:opacity-80 transition-all" />
            <rect x="105" y="220" width="25" height="100" rx="12" fill={getPartColor('leg_right')} onClick={() => setSelectedPart(selectedPart === 'leg_right' ? null : 'leg_right')} className="cursor-pointer hover:opacity-80 transition-all" />
            <ellipse cx="82" cy="340" rx="15" ry="10" fill={getPartColor('foot_left')} onClick={() => setSelectedPart(selectedPart === 'foot_left' ? null : 'foot_left')} className="cursor-pointer hover:opacity-80 transition-all" />
            <ellipse cx="118" cy="340" rx="15" ry="10" fill={getPartColor('foot_right')} onClick={() => setSelectedPart(selectedPart === 'foot_right' ? null : 'foot_right')} className="cursor-pointer hover:opacity-80 transition-all" />

            <text x="100" y="390" textAnchor="middle" fill="#6b7280" fontSize="12">Tap a body part</text>
          </svg>
        </div>

        {selectedPart && bodyPart && (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
            <div className="bg-green-600 text-white px-4 py-3 flex items-center justify-between">
              <h2 className="font-bold text-lg">{bodyPart.name}</h2>
              <button onClick={() => setSelectedPart(null)} className="p-1 hover:bg-green-700 rounded">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-4 space-y-4">
              <div className="flex items-start gap-3">
                <Info className="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" />
                <p className="text-gray-600 dark:text-gray-400">{bodyPart.info}</p>
              </div>

              {bodyPart.warning && (
                <div className="bg-amber-50 dark:bg-amber-900/20 rounded-lg p-3 border border-amber-200 dark:border-amber-800">
                  <div className="flex gap-2">
                    <AlertTriangle className="w-5 h-5 text-amber-600 flex-shrink-0" />
                    <p className="text-sm text-amber-700 dark:text-amber-300">{bodyPart.warning}</p>
                  </div>
                </div>
              )}

              <h3 className="font-semibold text-gray-800 dark:text-gray-100 pt-2">Common Issues:</h3>
              <div className="space-y-3">
                {bodyPart.commonIssues.map((issue, idx) => (
                  <div key={idx} className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3">
                    <h4 className="font-medium text-gray-800 dark:text-gray-100">{issue.name}</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{issue.treatment}</p>
                  </div>
                ))}
              </div>

              {bodyPart.emergencyLink && (
                <Link
                  to={bodyPart.emergencyLink}
                  className="block w-full text-center py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors"
                >
                  View Full Emergency Guide
                </Link>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
