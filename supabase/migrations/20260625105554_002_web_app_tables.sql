-- Simplified tables for web app (no auth required)

-- Emergency Contacts Table (simplified)
CREATE TABLE IF NOT EXISTS emergency_contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    relationship TEXT DEFAULT '',
    phone TEXT NOT NULL,
    is_primary BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- First Aid Items Table (simplified)
CREATE TABLE IF NOT EXISTS first_aid_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    quantity INTEGER DEFAULT 1,
    in_stock BOOLEAN DEFAULT true,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS but allow all access for anon users
ALTER TABLE emergency_contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE first_aid_items ENABLE ROW LEVEL SECURITY;

-- Allow all operations for anon and authenticated users
CREATE POLICY "allow_all_emergency_contacts" ON emergency_contacts FOR ALL
    USING (true) WITH CHECK (true);

CREATE POLICY "allow_all_first_aid_items" ON first_aid_items FOR ALL
    USING (true) WITH CHECK (true);