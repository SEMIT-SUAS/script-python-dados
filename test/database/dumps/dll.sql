SET search_path TO public;
--
-- PostgreSQL database dump
--

-- \restrict EboWzb1eJyHPZrjmfCeik6YN6T9cFPcEvcMSkaaogCA0T63aSl6H4dLmgnI5rUO

-- Dumped from database version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 17.9 (Debian 17.9-1.pgdg13+1)

-- SET statement_timeout = 0;
-- SET lock_timeout = 0;
-- SET idle_in_transaction_session_timeout = 0;
-- SET transaction_timeout = 0;
-- SET client_encoding = 'UTF8';
-- SET standard_conforming_strings = on;
-- SELECT pg_catalog.set_config('search_path', '', false);
-- SET check_function_bodies = false;
-- SET xmloption = content;
-- SET client_min_messages = warning;
-- SET row_security = off;

--
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


--
-- Name: unaccent; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA public;


--
-- Name: EXTENSION unaccent; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION unaccent IS 'text search dictionary that removes accents';


--
-- Name: user_profile; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.user_profile AS ENUM (
    'admin',
    'cadastro',
    'consulta'
);


ALTER TYPE public.user_profile OWNER TO postgres;

--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


-- ALTER FUNCTION public.update_updated_at_column() OWNER TO postgres;

-- SET default_tablespace = '';

-- SET default_table_access_method = heap;

--
-- Name: arquivos_digitais; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.arquivos_digitais (
    id integer NOT NULL,
    id_volume integer,
    nome_arquivo character varying(255) NOT NULL,
    path_arquivo text NOT NULL,
    tipo_mime character varying(100),
    tamanho_bytes bigint,
    hash_md5 character varying(32),
    ocr_status boolean DEFAULT false,
    conteudo_ocr text,
    uploaded_by integer,
    uploaded_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    chave_lote character varying(50),
    documento_tsvector tsvector
);


-- ALTER TABLE public.arquivos_digitais OWNER TO postgres;

--
-- Name: arquivos_digitais_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.arquivos_digitais_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER SEQUENCE public.arquivos_digitais_id_seq OWNER TO postgres;

--
-- Name: arquivos_digitais_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.arquivos_digitais_id_seq OWNED BY public.arquivos_digitais.id;


--
-- Name: discos_servidores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.discos_servidores (
    id integer NOT NULL,
    nome_disco_servidor character varying(255) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


-- ALTER TABLE public.discos_servidores OWNER TO postgres;

--
-- Name: discos_servidores_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.discos_servidores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER SEQUENCE public.discos_servidores_id_seq OWNER TO postgres;

--
-- Name: discos_servidores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.discos_servidores_id_seq OWNED BY public.discos_servidores.id;


--
-- Name: empresas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.empresas (
    id integer NOT NULL,
    razao_social character varying(255) NOT NULL,
    cnpj character varying(18) NOT NULL,
    nome_fantasia character varying(255),
    tags text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


-- ALTER TABLE public.empresas OWNER TO postgres;

--
-- Name: empresas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.empresas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER SEQUENCE public.empresas_id_seq OWNER TO postgres;

--
-- Name: empresas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.empresas_id_seq OWNED BY public.empresas.id;


--
-- Name: enderecos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.enderecos (
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    nome_endereco character varying(255)
);


-- ALTER TABLE public.enderecos OWNER TO postgres;

--
-- Name: enderecos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.enderecos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER SEQUENCE public.enderecos_id_seq OWNER TO postgres;

--
-- Name: enderecos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.enderecos_id_seq OWNED BY public.enderecos.id;


--
-- Name: estados_conservacao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estados_conservacao (
    id integer NOT NULL,
    descricao character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


-- ALTER TABLE public.estados_conservacao OWNER TO postgres;

--
-- Name: estados_conservacao_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.estados_conservacao_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER SEQUENCE public.estados_conservacao_id_seq OWNER TO postgres;

--
-- Name: estados_conservacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.estados_conservacao_id_seq OWNED BY public.estados_conservacao.id;


--
-- Name: estantes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estantes (
    id integer NOT NULL,
    id_setor integer NOT NULL,
    id_endereco integer NOT NULL,
    codigo_estante character varying(100) NOT NULL,
    numero_prateleiras integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


-- ALTER TABLE public.estantes OWNER TO postgres;

--
-- Name: estantes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.estantes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER SEQUENCE public.estantes_id_seq OWNER TO postgres;

--
-- Name: estantes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.estantes_id_seq OWNED BY public.estantes.id;


--
-- Name: logs_auditoria; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.logs_auditoria (
    id integer NOT NULL,
    id_usuario integer,
    acao_realizada character varying(255) NOT NULL,
    detalhes text,
    ip_acesso character varying(45),
    timestamp_acao timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


-- ALTER TABLE public.logs_auditoria OWNER TO postgres;

--
-- Name: logs_auditoria_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.logs_auditoria_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER SEQUENCE public.logs_auditoria_id_seq OWNER TO postgres;

--
-- Name: logs_auditoria_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.logs_auditoria_id_seq OWNED BY public.logs_auditoria.id;


--
-- Name: lotacao_atual; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lotacao_atual (
    id integer NOT NULL,
    id_secretaria integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


-- ALTER TABLE public.lotacao_atual OWNER TO postgres;

--
-- Name: lotacao_atual_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.lotacao_atual_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER SEQUENCE public.lotacao_atual_id_seq OWNER TO postgres;

--
-- Name: lotacao_atual_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.lotacao_atual_id_seq OWNED BY public.lotacao_atual.id;


--
-- Name: pastas_digitais; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pastas_digitais (
    id integer NOT NULL,
    nome_pasta character varying(255) NOT NULL,
    caminho_pasta text NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    id_disco_servidor integer
);


-- ALTER TABLE public.pastas_digitais OWNER TO postgres;

--
-- Name: pastas_digitais_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pastas_digitais_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER SEQUENCE public.pastas_digitais_id_seq OWNER TO postgres;

--
-- Name: pastas_digitais_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pastas_digitais_id_seq OWNED BY public.pastas_digitais.id;


--
-- Name: permissoes_usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.permissoes_usuario (
    id bigint NOT NULL,
    id_usuario bigint NOT NULL,
    id_secretaria bigint NOT NULL,
    id_tipo_documental bigint,
    acesso_total_secretaria boolean DEFAULT false NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


-- ALTER TABLE public.permissoes_usuario OWNER TO postgres;

--
-- Name: permissoes_usuario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.permissoes_usuario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER SEQUENCE public.permissoes_usuario_id_seq OWNER TO postgres;

--
-- Name: permissoes_usuario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.permissoes_usuario_id_seq OWNED BY public.permissoes_usuario.id;


--
-- Name: prateleiras; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prateleiras (
    id integer NOT NULL,
    numero_prateleira character varying(50) NOT NULL,
    id_estantes integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


-- ALTER TABLE public.prateleiras OWNER TO postgres;

--
-- Name: prateleiras_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.prateleiras_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER SEQUENCE public.prateleiras_id_seq OWNER TO postgres;

--
-- Name: prateleiras_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.prateleiras_id_seq OWNED BY public.prateleiras.id;


--
-- Name: secretarias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.secretarias (
    id integer NOT NULL,
    nome_secretaria character varying(255) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


-- ALTER TABLE public.secretarias OWNER TO postgres;

--
-- Name: secretarias_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.secretarias_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER SEQUENCE public.secretarias_id_seq OWNER TO postgres;

--
-- Name: secretarias_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.secretarias_id_seq OWNED BY public.secretarias.id;


--
-- Name: servidores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.servidores (
    id integer NOT NULL,
    nome_completo character varying(255) NOT NULL,
    cpf character varying(14) NOT NULL,
    matricula character varying(50),
    cargo character varying(100),
    tags text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    id_secretaria integer,
    id_lotacao_atual integer
);


-- ALTER TABLE public.servidores OWNER TO postgres;

--
-- Name: servidores_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.servidores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER SEQUENCE public.servidores_id_seq OWNER TO postgres;

--
-- Name: servidores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.servidores_id_seq OWNED BY public.servidores.id;


--
-- Name: setores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.setores (
    id integer NOT NULL,
    nome character varying(255) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    id_endereco integer
);


-- ALTER TABLE public.setores OWNER TO postgres;

--
-- Name: setores_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.setores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER SEQUENCE public.setores_id_seq OWNER TO postgres;

--
-- Name: setores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.setores_id_seq OWNED BY public.setores.id;


--
-- Name: tipos_documentais; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tipos_documentais (
    id integer NOT NULL,
    tipo_documento character varying(150) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


-- ALTER TABLE public.tipos_documentais OWNER TO postgres;

--
-- Name: tipos_documentais_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tipos_documentais_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER SEQUENCE public.tipos_documentais_id_seq OWNER TO postgres;

--
-- Name: tipos_documentais_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tipos_documentais_id_seq OWNED BY public.tipos_documentais.id;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    nome character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    cpf character varying(14),
    senha character varying(255) NOT NULL,
    perfil character varying(50) NOT NULL,
    id_setor integer,
    ativo boolean DEFAULT true,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    acesso_total_sistema boolean DEFAULT false
);


-- ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER SEQUENCE public.usuarios_id_seq OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- Name: volumes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.volumes (
    id integer NOT NULL,
    titulo character varying(255) NOT NULL,
    data_documento date,
    quantidade_folhas integer,
    tags text,
    created_by integer,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    id_servidor integer,
    id_empresa integer,
    numero_volume character varying(100),
    id_tipo_documental integer NOT NULL,
    id_estado_conservacao integer,
    id_secretaria integer,
    id_discos_servidores integer,
    id_enderecos integer,
    id_setores integer,
    id_estantes integer,
    descricao_volumes text,
    id_arquivos_digitais integer,
    ativo boolean DEFAULT true NOT NULL,
    descricao_inativo text,
    status_emprestado boolean,
    descricao_emprestado text,
    tipo_folha character varying(50),
    opcao_ocr character varying(20),
    id_prateleiras integer,
    id_pastas_digitais bigint,
    origem character varying(100),
    chave_lote character varying(50)
);


-- ALTER TABLE public.volumes OWNER TO postgres;

--
-- Name: volumes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.volumes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER SEQUENCE public.volumes_id_seq OWNER TO postgres;

--
-- Name: volumes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.volumes_id_seq OWNED BY public.volumes.id;


--
-- Name: arquivos_digitais id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arquivos_digitais ALTER COLUMN id SET DEFAULT nextval('public.arquivos_digitais_id_seq'::regclass);


--
-- Name: discos_servidores id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discos_servidores ALTER COLUMN id SET DEFAULT nextval('public.discos_servidores_id_seq'::regclass);


--
-- Name: empresas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas ALTER COLUMN id SET DEFAULT nextval('public.empresas_id_seq'::regclass);


--
-- Name: enderecos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enderecos ALTER COLUMN id SET DEFAULT nextval('public.enderecos_id_seq'::regclass);


--
-- Name: estados_conservacao id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estados_conservacao ALTER COLUMN id SET DEFAULT nextval('public.estados_conservacao_id_seq'::regclass);


--
-- Name: estantes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estantes ALTER COLUMN id SET DEFAULT nextval('public.estantes_id_seq'::regclass);


--
-- Name: logs_auditoria id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_auditoria ALTER COLUMN id SET DEFAULT nextval('public.logs_auditoria_id_seq'::regclass);


--
-- Name: lotacao_atual id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lotacao_atual ALTER COLUMN id SET DEFAULT nextval('public.lotacao_atual_id_seq'::regclass);


--
-- Name: pastas_digitais id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pastas_digitais ALTER COLUMN id SET DEFAULT nextval('public.pastas_digitais_id_seq'::regclass);


--
-- Name: permissoes_usuario id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissoes_usuario ALTER COLUMN id SET DEFAULT nextval('public.permissoes_usuario_id_seq'::regclass);


--
-- Name: prateleiras id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prateleiras ALTER COLUMN id SET DEFAULT nextval('public.prateleiras_id_seq'::regclass);


--
-- Name: secretarias id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.secretarias ALTER COLUMN id SET DEFAULT nextval('public.secretarias_id_seq'::regclass);


--
-- Name: servidores id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servidores ALTER COLUMN id SET DEFAULT nextval('public.servidores_id_seq'::regclass);


--
-- Name: setores id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.setores ALTER COLUMN id SET DEFAULT nextval('public.setores_id_seq'::regclass);


--
-- Name: tipos_documentais id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_documentais ALTER COLUMN id SET DEFAULT nextval('public.tipos_documentais_id_seq'::regclass);


--
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- Name: volumes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volumes ALTER COLUMN id SET DEFAULT nextval('public.volumes_id_seq'::regclass);


--
-- Name: arquivos_digitais arquivos_digitais_path_arquivo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arquivos_digitais
    ADD CONSTRAINT arquivos_digitais_path_arquivo_key UNIQUE (path_arquivo);


--
-- Name: arquivos_digitais arquivos_digitais_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arquivos_digitais
    ADD CONSTRAINT arquivos_digitais_pkey PRIMARY KEY (id);


--
-- Name: discos_servidores discos_servidores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discos_servidores
    ADD CONSTRAINT discos_servidores_pkey PRIMARY KEY (id);


--
-- Name: empresas empresas_cnpj_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_cnpj_key UNIQUE (cnpj);


--
-- Name: empresas empresas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_pkey PRIMARY KEY (id);


--
-- Name: enderecos enderecos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enderecos
    ADD CONSTRAINT enderecos_pkey PRIMARY KEY (id);


--
-- Name: estados_conservacao estados_conservacao_descricao_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estados_conservacao
    ADD CONSTRAINT estados_conservacao_descricao_key UNIQUE (descricao);


--
-- Name: estados_conservacao estados_conservacao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estados_conservacao
    ADD CONSTRAINT estados_conservacao_pkey PRIMARY KEY (id);


--
-- Name: estantes estantes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estantes
    ADD CONSTRAINT estantes_pkey PRIMARY KEY (id);


--
-- Name: logs_auditoria logs_auditoria_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_auditoria
    ADD CONSTRAINT logs_auditoria_pkey PRIMARY KEY (id);


--
-- Name: lotacao_atual lotacao_atual_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lotacao_atual
    ADD CONSTRAINT lotacao_atual_pkey PRIMARY KEY (id);


--
-- Name: pastas_digitais pastas_digitais_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pastas_digitais
    ADD CONSTRAINT pastas_digitais_pkey PRIMARY KEY (id);


--
-- Name: permissoes_usuario permissoes_usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissoes_usuario
    ADD CONSTRAINT permissoes_usuario_pkey PRIMARY KEY (id);


--
-- Name: prateleiras prateleiras_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prateleiras
    ADD CONSTRAINT prateleiras_pkey PRIMARY KEY (id);


--
-- Name: secretarias secretarias_nome_secretaria_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.secretarias
    ADD CONSTRAINT secretarias_nome_secretaria_key UNIQUE (nome_secretaria);


--
-- Name: secretarias secretarias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.secretarias
    ADD CONSTRAINT secretarias_pkey PRIMARY KEY (id);


--
-- Name: servidores servidores_cpf_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servidores
    ADD CONSTRAINT servidores_cpf_key UNIQUE (cpf);


--
-- Name: servidores servidores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servidores
    ADD CONSTRAINT servidores_pkey PRIMARY KEY (id);


--
-- Name: setores setores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.setores
    ADD CONSTRAINT setores_pkey PRIMARY KEY (id);


--
-- Name: tipos_documentais tipos_documentais_descricao_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_documentais
    ADD CONSTRAINT tipos_documentais_descricao_key UNIQUE (tipo_documento);


--
-- Name: tipos_documentais tipos_documentais_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_documentais
    ADD CONSTRAINT tipos_documentais_pkey PRIMARY KEY (id);


--
-- Name: usuarios usuarios_cpf_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_cpf_key UNIQUE (cpf);


--
-- Name: usuarios usuarios_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- Name: volumes volumes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volumes
    ADD CONSTRAINT volumes_pkey PRIMARY KEY (id);


--
-- Name: idx_arquivos_busca_fulltext; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_arquivos_busca_fulltext ON public.arquivos_digitais USING gin (documento_tsvector);


--
-- Name: idx_arquivos_conteudo_ocr_trgm; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_arquivos_conteudo_ocr_trgm ON public.arquivos_digitais USING gin (conteudo_ocr public.gin_trgm_ops);


--
-- Name: idx_arquivos_digitais_conteudo_ocr_gin; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_arquivos_digitais_conteudo_ocr_gin ON public.arquivos_digitais USING gin (conteudo_ocr public.gin_trgm_ops);


--
-- Name: idx_arquivos_ocr_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_arquivos_ocr_status ON public.arquivos_digitais USING btree (ocr_status);


--
-- Name: idx_empresas_razao_social_trgm; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_empresas_razao_social_trgm ON public.empresas USING gin (razao_social public.gin_trgm_ops);


--
-- Name: idx_ocr_trgm; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ocr_trgm ON public.arquivos_digitais USING gin (conteudo_ocr public.gin_trgm_ops);


--
-- Name: idx_permissoes_usuario_id_secretaria; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_permissoes_usuario_id_secretaria ON public.permissoes_usuario USING btree (id_secretaria);


--
-- Name: idx_permissoes_usuario_id_tipo_documental; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_permissoes_usuario_id_tipo_documental ON public.permissoes_usuario USING btree (id_tipo_documental);


--
-- Name: idx_permissoes_usuario_id_usuario; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_permissoes_usuario_id_usuario ON public.permissoes_usuario USING btree (id_usuario);


--
-- Name: idx_prateleira_estante_unique; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_prateleira_estante_unique ON public.prateleiras USING btree (numero_prateleira, id_estantes);


--
-- Name: idx_prateleiras_estante; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_prateleiras_estante ON public.prateleiras USING btree (id_estantes);


--
-- Name: idx_servidores_nome_trgm; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_servidores_nome_trgm ON public.servidores USING gin (nome_completo public.gin_trgm_ops);


--
-- Name: idx_volumes_data_documento_desc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_volumes_data_documento_desc ON public.volumes USING btree (data_documento DESC);


--
-- Name: idx_volumes_numero_volume; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_volumes_numero_volume ON public.volumes USING btree (numero_volume);


--
-- Name: idx_volumes_numero_volume_trgm; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_volumes_numero_volume_trgm ON public.volumes USING gin (numero_volume public.gin_trgm_ops);


--
-- Name: idx_volumes_prateleira; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_volumes_prateleira ON public.volumes USING btree (id_prateleiras);


--
-- Name: idx_volumes_titulo_trgm; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_volumes_titulo_trgm ON public.volumes USING gin (titulo public.gin_trgm_ops);


--
-- Name: arquivos_digitais arquivos_digital_tsvector_update; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER arquivos_digital_tsvector_update BEFORE INSERT OR UPDATE ON public.arquivos_digitais FOR EACH ROW EXECUTE FUNCTION tsvector_update_trigger('documento_tsvector', 'pg_catalog.portuguese', 'conteudo_ocr');


--
-- Name: prateleiras update_prateleiras_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_prateleiras_updated_at BEFORE UPDATE ON public.prateleiras FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: arquivos_digitais arquivos_digitais_id_volume_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arquivos_digitais
    ADD CONSTRAINT arquivos_digitais_id_volume_fkey FOREIGN KEY (id_volume) REFERENCES public.volumes(id) ON DELETE CASCADE;


--
-- Name: arquivos_digitais arquivos_digitais_uploaded_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arquivos_digitais
    ADD CONSTRAINT arquivos_digitais_uploaded_by_fkey FOREIGN KEY (uploaded_by) REFERENCES public.usuarios(id);


--
-- Name: volumes discos_servidores_id_volume_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volumes
    ADD CONSTRAINT discos_servidores_id_volume_fkey FOREIGN KEY (id_discos_servidores) REFERENCES public.discos_servidores(id) ON DELETE CASCADE;


--
-- Name: volumes enderecos_id_volume_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volumes
    ADD CONSTRAINT enderecos_id_volume_fkey FOREIGN KEY (id_enderecos) REFERENCES public.enderecos(id) ON DELETE CASCADE;


--
-- Name: volumes estantes_id_volume_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volumes
    ADD CONSTRAINT estantes_id_volume_fkey FOREIGN KEY (id_estantes) REFERENCES public.estantes(id) ON DELETE CASCADE;


--
-- Name: volumes fk_arquivo_digital; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volumes
    ADD CONSTRAINT fk_arquivo_digital FOREIGN KEY (id_arquivos_digitais) REFERENCES public.arquivos_digitais(id) ON DELETE SET NULL;


--
-- Name: arquivos_digitais fk_arquivo_volume; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arquivos_digitais
    ADD CONSTRAINT fk_arquivo_volume FOREIGN KEY (id_volume) REFERENCES public.volumes(id) ON DELETE SET NULL;


--
-- Name: pastas_digitais fk_disco_servidor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pastas_digitais
    ADD CONSTRAINT fk_disco_servidor FOREIGN KEY (id_disco_servidor) REFERENCES public.discos_servidores(id) ON DELETE CASCADE;


--
-- Name: estantes fk_endereco; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estantes
    ADD CONSTRAINT fk_endereco FOREIGN KEY (id_endereco) REFERENCES public.enderecos(id);


--
-- Name: estantes fk_estante_endereco; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estantes
    ADD CONSTRAINT fk_estante_endereco FOREIGN KEY (id_endereco) REFERENCES public.enderecos(id) ON DELETE CASCADE;


--
-- Name: estantes fk_estante_setor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estantes
    ADD CONSTRAINT fk_estante_setor FOREIGN KEY (id_setor) REFERENCES public.setores(id) ON DELETE CASCADE;


--
-- Name: lotacao_atual fk_lotacao_secretaria; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lotacao_atual
    ADD CONSTRAINT fk_lotacao_secretaria FOREIGN KEY (id_secretaria) REFERENCES public.secretarias(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: permissoes_usuario fk_permissoes_secretaria; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissoes_usuario
    ADD CONSTRAINT fk_permissoes_secretaria FOREIGN KEY (id_secretaria) REFERENCES public.secretarias(id) ON DELETE CASCADE;


--
-- Name: permissoes_usuario fk_permissoes_tipo_documental; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissoes_usuario
    ADD CONSTRAINT fk_permissoes_tipo_documental FOREIGN KEY (id_tipo_documental) REFERENCES public.tipos_documentais(id) ON DELETE CASCADE;


--
-- Name: permissoes_usuario fk_permissoes_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissoes_usuario
    ADD CONSTRAINT fk_permissoes_usuario FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id) ON DELETE CASCADE;


--
-- Name: prateleiras fk_prateleira_estante; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prateleiras
    ADD CONSTRAINT fk_prateleira_estante FOREIGN KEY (id_estantes) REFERENCES public.estantes(id) ON DELETE CASCADE;


--
-- Name: servidores fk_servidores_lotacao_atual; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servidores
    ADD CONSTRAINT fk_servidores_lotacao_atual FOREIGN KEY (id_lotacao_atual) REFERENCES public.lotacao_atual(id) ON DELETE SET NULL;


--
-- Name: servidores fk_servidores_secretaria; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servidores
    ADD CONSTRAINT fk_servidores_secretaria FOREIGN KEY (id_secretaria) REFERENCES public.secretarias(id);


--
-- Name: setores fk_setor_endereco; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.setores
    ADD CONSTRAINT fk_setor_endereco FOREIGN KEY (id_endereco) REFERENCES public.enderecos(id) ON DELETE SET NULL;


--
-- Name: volumes fk_tipo_documental; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volumes
    ADD CONSTRAINT fk_tipo_documental FOREIGN KEY (id_tipo_documental) REFERENCES public.tipos_documentais(id);


--
-- Name: volumes fk_volume_prateleira; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volumes
    ADD CONSTRAINT fk_volume_prateleira FOREIGN KEY (id_prateleiras) REFERENCES public.prateleiras(id) ON DELETE SET NULL;


--
-- Name: volumes fk_volumes_empresa; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volumes
    ADD CONSTRAINT fk_volumes_empresa FOREIGN KEY (id_empresa) REFERENCES public.empresas(id);


--
-- Name: volumes fk_volumes_pastas_digitais; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volumes
    ADD CONSTRAINT fk_volumes_pastas_digitais FOREIGN KEY (id_pastas_digitais) REFERENCES public.pastas_digitais(id);


--
-- Name: volumes fk_volumes_servidor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volumes
    ADD CONSTRAINT fk_volumes_servidor FOREIGN KEY (id_servidor) REFERENCES public.servidores(id);


--
-- Name: logs_auditoria logs_auditoria_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_auditoria
    ADD CONSTRAINT logs_auditoria_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id);


--
-- Name: volumes setores_id_volume_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volumes
    ADD CONSTRAINT setores_id_volume_fkey FOREIGN KEY (id_setores) REFERENCES public.setores(id) ON DELETE CASCADE;


--
-- Name: usuarios usuarios_id_setor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_id_setor_fkey FOREIGN KEY (id_setor) REFERENCES public.setores(id);


--
-- Name: volumes volumes_id_estado_conservacao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volumes
    ADD CONSTRAINT volumes_id_estado_conservacao_fkey FOREIGN KEY (id_estado_conservacao) REFERENCES public.estados_conservacao(id);


--
-- Name: volumes volumes_id_secretaria_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volumes
    ADD CONSTRAINT volumes_id_secretaria_fkey FOREIGN KEY (id_secretaria) REFERENCES public.secretarias(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: volumes volumes_id_tipo_documental_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.volumes
    ADD CONSTRAINT volumes_id_tipo_documental_fkey FOREIGN KEY (id_tipo_documental) REFERENCES public.tipos_documentais(id);


--
-- PostgreSQL database dump complete
--

-- \unrestrict EboWzb1eJyHPZrjmfCeik6YN6T9cFPcEvcMSkaaogCA0T63aSl6H4dLmgnI5rUO

