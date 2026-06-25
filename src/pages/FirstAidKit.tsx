import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft, Plus, Check, Trash2, Edit2, Briefcase, AlertTriangle } from 'lucide-react'
import { supabase } from '../lib/supabase'

interface FirstAidItem {
  id: string
  name: string
  quantity: number
  in_stock: boolean
  notes?: string
}

const defaultItems: { name: string; quantity: number }[] = [
  { name: 'Adhesive bandages (assorted sizes)', quantity: 20 },
  { name: 'Sterile gauze pads', quantity: 10 },
  { name: 'Adhesive tape', quantity: 2 },
  { name: 'Elastic bandage', quantity: 2 },
  { name: 'Antiseptic wipes', quantity: 10 },
  { name: 'Antiseptic ointment', quantity: 1 },
  { name: 'Instant cold pack', quantity: 2 },
  { name: 'Disposable gloves', quantity: 4 },
  { name: 'Tweezers', quantity: 1 },
  { name: 'Scissors', quantity: 1 },
  { name: 'Pain relievers (aspirin/ibuprofen)', quantity: 1 },
  { name: 'Antihistamine (for allergic reactions)', quantity: 1 },
  { name: 'Emergency blanket', quantity: 1 },
  { name: 'Flashlight with batteries', quantity: 1 },
  { name: 'First aid manual', quantity: 1 },
]

export default function FirstAidKit() {
  const [items, setItems] = useState<FirstAidItem[]>([])
  const [showAddModal, setShowAddModal] = useState(false)
  const [editingItem, setEditingItem] = useState<FirstAidItem | null>(null)
  const [formData, setFormData] = useState({ name: '', quantity: 1, notes: '' })

  useEffect(() => {
    loadItems()
  }, [])

  const loadItems = async () => {
    try {
      const { data, error } = await supabase
        .from('first_aid_items')
        .select('*')
        .order('name')

      if (error) throw error

      if (data && data.length > 0) {
        setItems(data)
      } else {
        const { error: insertError } = await supabase
          .from('first_aid_items')
          .insert(defaultItems.map(item => ({
            ...item,
            in_stock: true,
          })))

        if (!insertError) {
          loadItems()
        }
      }
    } catch (err) {
      console.error('Error loading items:', err)
    }
  }

  const toggleInStock = async (id: string, currentStatus: boolean) => {
    try {
      const { error } = await supabase
        .from('first_aid_items')
        .update({ in_stock: !currentStatus })
        .eq('id', id)

      if (!error) {
        loadItems()
      }
    } catch (err) {
      console.error('Error updating item:', err)
    }
  }

  const handleSave = async () => {
    if (!formData.name) return

    try {
      if (editingItem) {
        const { error } = await supabase
          .from('first_aid_items')
          .update({
            name: formData.name,
            quantity: formData.quantity,
            notes: formData.notes,
          })
          .eq('id', editingItem.id)

        if (error) throw error
      } else {
        const { error } = await supabase
          .from('first_aid_items')
          .insert({
            name: formData.name,
            quantity: formData.quantity,
            notes: formData.notes,
            in_stock: true,
          })

        if (error) throw error
      }

      closeModal()
      loadItems()
    } catch (err) {
      console.error('Error saving item:', err)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this item?')) return

    try {
      const { error } = await supabase
        .from('first_aid_items')
        .delete()
        .eq('id', id)

      if (!error) {
        loadItems()
      }
    } catch (err) {
      console.error('Error deleting item:', err)
    }
  }

  const openEditModal = (item: FirstAidItem) => {
    setEditingItem(item)
    setFormData({
      name: item.name,
      quantity: item.quantity,
      notes: item.notes || '',
    })
    setShowAddModal(true)
  }

  const closeModal = () => {
    setShowAddModal(false)
    setEditingItem(null)
    setFormData({ name: '', quantity: 1, notes: '' })
  }

  const inStockCount = items.filter(i => i.in_stock).length
  const totalCount = items.length
  const missingCount = totalCount - inStockCount

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <header className="bg-amber-600 text-white px-4 py-4 sticky top-0 z-10 shadow-lg">
        <div className="max-w-lg mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link to="/" className="p-2 hover:bg-amber-700 rounded-lg">
              <ArrowLeft className="w-6 h-6" />
            </Link>
            <h1 className="text-xl font-bold">First Aid Kit</h1>
          </div>
          <button
            onClick={() => setShowAddModal(true)}
            className="p-2 hover:bg-amber-700 rounded-lg"
          >
            <Plus className="w-6 h-6" />
          </button>
        </div>
      </header>

      <main className="max-w-lg mx-auto px-4 py-6 space-y-4">
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-md border border-gray-100 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center">
                <Briefcase className="w-6 h-6 text-amber-600 dark:text-amber-400" />
              </div>
              <div>
                <h3 className="font-full text-gray-800 dark:text-gray-100">Kit Status</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {inStockCount} of {totalCount} items ready
                </p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-green-600 dark:text-green-400">{inStockCount}</div>
              <div className="text-xs text-gray-500 dark:text-gray-400">in stock</div>
            </div>
          </div>

          <div className="mt-4 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-green-500 transition-all"
              style={{ width: `${(inStockCount / totalCount) * 100}%` }}
            />
          </div>
        </div>

        {missingCount > 0 && (
          <div className="bg-amber-50 dark:bg-amber-900/20 rounded-xl p-4 border border-amber-200 dark:border-amber-800">
            <div className="flex gap-3">
              <AlertTriangle className="w-5 h-5 text-amber-600 flex-shrink-0" />
              <p className="text-sm text-amber-700 dark:text-amber-300">
                {missingCount} item{missingCount !== 1 ? 's' : ''} need to be restocked. Check your kit regularly!
              </p>
            </div>
          </div>
        )}

        <div className="space-y-2">
          {items.map((item) => (
            <div
              key={item.id}
              className={`bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm border ${
                item.in_stock
                  ? 'border-gray-100 dark:border-gray-700'
                  : 'border-red-200 dark:border-red-900'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3 flex-1">
                  <button
                    onClick={() => toggleInStock(item.id, item.in_stock)}
                    className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${
                      item.in_stock
                        ? 'bg-green-600 border-green-600 text-white'
                        : 'border-gray-300 dark:border-gray-600'
                    }`}
                  >
                    {item.in_stock && <Check className="w-4 h-4" />}
                  </button>
                  <div className="flex-1">
                    <h3 className={`font-medium ${item.in_stock ? 'text-gray-800 dark:text-gray-100' : 'text-gray-400 dark:text-gray-500'}`}>
                      {item.name}
                    </h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Qty: {item.quantity} {item.notes && `• ${item.notes}`}
                    </p>
                  </div>
                </div>
                <div className="flex gap-1">
                  <button
                    onClick={() => openEditModal(item)}
                    className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg text-gray-500 dark:text-gray-400"
                  >
                    <Edit2 className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(item.id)}
                    className="p-2 hover:bg-red-100 dark:hover:bg-red-900/30 rounded-lg text-red-500 dark:text-red-400"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>

      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 w-full max-w-md shadow-xl">
            <h2 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4">
              {editingItem ? 'Edit Item' : 'Add Item'}
            </h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Item Name
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                  placeholder="Item name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Quantity
                </label>
                <input
                  type="number"
                  min="1"
                  value={formData.quantity}
                  onChange={(e) => setFormData({ ...formData, quantity: parseInt(e.target.value) || 1 })}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Notes (optional)
                </label>
                <input
                  type="text"
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                  placeholder="e.g., Check expiration date"
                />
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={closeModal}
                className="flex-1 py-2 px-4 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg font-medium hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                className="flex-1 py-2 px-4 bg-amber-600 text-white rounded-lg font-medium hover:bg-amber-700 transition-colors"
              >
                Save Item
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
