create extension if not exists "uuid-ossp";

create table if not exists public.students (
  id uuid primary key default uuid_generate_v4(), 
  first_name text not null, 
  last_name text not null,
  program text,
  year_level integer,
  email text unique not null,
  status text default 'active',
  created_at timestamp default now()
);

create table if not exists public.equipment (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  category text,
  serial_number text unique,
  condition text default 'Good',
  availability_status text default 'Available',
  created_at timestamp default now()
);

create table if not exists public.loans (
  id uuid primary key default uuid_generate_v4(),
  student_id uuid not null references public.students(id) on delete restrict,
  equipment_id uuid not null references public.equipment(id) on delete restrict,
  date_borrowed date not null,
  date_due date not null,
  date_returned date,
  status text default 'Borrowed',
  created_at timestamp default now()
);

create table if not exists public.staff (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  email text unique,
  role text default 'approver',
  created_at timestamp default now()
);

create table if not exists public.email_logs (
  id uuid primary key default uuid_generate_v4(),
  loan_id uuid not null references public.loans(id) on delete cascade,
  recipient_email text not null,
  email_type text not null,
  sent_at timestamp default now(),
  status text default 'sent'
);

create table if not exists public.audit_logs (
  id uuid primary key default uuid_generate_v4(),
  action text not null,
  table_name text not null,
  record_id uuid,
  details jsonb,
  created_at timestamp default now()
);
