import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://zwblgqecoumpwkbmmlua.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp3YmxncWVjb3VtcHdrYm1tbHVhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk3NDg2NzQsImV4cCI6MjA4NTMyNDY3NH0.-W00jf8MUkND_LtH_jr_O0j5mZk8HtFQ2JvcgLm53mw';

export const supabase = createClient(supabaseUrl, supabaseKey);
