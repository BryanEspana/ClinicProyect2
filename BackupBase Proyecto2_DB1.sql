PGDMP         .                {            CentroMedico    15.2    15.1 -                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16439    CentroMedico    DATABASE     z   CREATE DATABASE "CentroMedico" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE "CentroMedico";
                postgres    false            �            1255    16572    historial_trigger()    FUNCTION     �  CREATE FUNCTION public.historial_trigger() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    jsonb_dataNew JSONB;
	jsonb_dataOld JSONB;
BEGIN
    IF (TG_OP = 'INSERT') THEN-- ---------------------------------------------------------------INSERT
        jsonb_dataNew = row_to_json(NEW.*);
        INSERT INTO bitacora (fecha_modificacion, id_historial_mod, type_mod, valor_nue)
        VALUES (CURRENT_TIMESTAMP, NEW.id_historial, 'I', jsonb_dataNew);
        RETURN NEW;
    ELSIF (TG_OP = 'UPDATE') THEN -- ------------------------------------------------------------UPDATE
        jsonb_dataNew = row_to_json(NEW.*);
		jsonb_dataOld = row_to_json(OLD.*);
        INSERT INTO bitacora (fecha_modificacion, id_historial_mod, type_mod, valor_pre, valor_nue)
        VALUES (CURRENT_TIMESTAMP, OLD.id_historial, 'U', jsonb_dataOld, jsonb_dataNew);
        RETURN NEW;
    ELSIF (TG_OP = 'DELETE') THEN -- -------------------------------------------------------------DELETE
        jsonb_dataOld = row_to_json(OLD.*);
        INSERT INTO bitacora (fecha_modificacion, id_historial_mod, type_mod, valor_pre)
        VALUES (CURRENT_TIMESTAMP,OLD.id_historial, 'D', jsonb_dataOld);
        RETURN OLD;
    END IF;
END;
$$;
 *   DROP FUNCTION public.historial_trigger();
       public          postgres    false            �            1259    16595    bitacora    TABLE       CREATE TABLE public.bitacora (
    id_cambio integer NOT NULL,
    id_historial_mod integer,
    fecha_modificacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    usuario integer,
    type_mod character(1) NOT NULL,
    valor_pre jsonb,
    valor_nue jsonb
);
    DROP TABLE public.bitacora;
       public         heap    postgres    false            �            1259    16594    bitacora_id_cambio_seq    SEQUENCE     �   CREATE SEQUENCE public.bitacora_id_cambio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.bitacora_id_cambio_seq;
       public          postgres    false    223                       0    0    bitacora_id_cambio_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.bitacora_id_cambio_seq OWNED BY public.bitacora.id_cambio;
          public          postgres    false    222            �            1259    16440 
   enfermedad    TABLE     j   CREATE TABLE public.enfermedad (
    id_enfermedad integer NOT NULL,
    nombre character varying(100)
);
    DROP TABLE public.enfermedad;
       public         heap    postgres    false            �            1259    16443 	   historial    TABLE     �  CREATE TABLE public.historial (
    id_historial integer NOT NULL,
    fecha date NOT NULL,
    herencia text NOT NULL,
    tratamiento text NOT NULL,
    evolucion text NOT NULL,
    estado character varying(100) NOT NULL,
    comentario text NOT NULL,
    id_lugar integer NOT NULL,
    id_paciente integer NOT NULL,
    id_medico integer NOT NULL,
    id_enfermedad integer NOT NULL
);
    DROP TABLE public.historial;
       public         heap    postgres    false            �            1259    16448 
   inventario    TABLE     �   CREATE TABLE public.inventario (
    id_inventario integer NOT NULL,
    id_lugar integer NOT NULL,
    id_utencilio integer NOT NULL,
    cantidad integer NOT NULL,
    expiracion date NOT NULL
);
    DROP TABLE public.inventario;
       public         heap    postgres    false            �            1259    16451    lugar    TABLE     �   CREATE TABLE public.lugar (
    id_lugar integer NOT NULL,
    nombre character varying(50) NOT NULL,
    localizacion text NOT NULL
);
    DROP TABLE public.lugar;
       public         heap    postgres    false            �            1259    16456    medico    TABLE     5  CREATE TABLE public.medico (
    id_medico integer NOT NULL,
    nombre character varying(50) NOT NULL,
    direccion text NOT NULL,
    telefono character varying(15) NOT NULL,
    numcolegiado character varying(15) NOT NULL,
    especialidad character varying(40) NOT NULL,
    id_lugar integer NOT NULL
);
    DROP TABLE public.medico;
       public         heap    postgres    false            �            1259    16461    paciente    TABLE     (  CREATE TABLE public.paciente (
    id_paciente integer NOT NULL,
    nombre character varying(50) NOT NULL,
    masacorporal double precision NOT NULL,
    altura double precision NOT NULL,
    adicciones text NOT NULL,
    telefono character varying(15) NOT NULL,
    direccion text NOT NULL
);
    DROP TABLE public.paciente;
       public         heap    postgres    false            �            1259    16466    usuario    TABLE     �   CREATE TABLE public.usuario (
    id_medico integer NOT NULL,
    usuario character varying(200),
    password character varying(200)
);
    DROP TABLE public.usuario;
       public         heap    postgres    false            �            1259    16469    utencilio_med    TABLE     �   CREATE TABLE public.utencilio_med (
    id_utencilio integer NOT NULL,
    nombre character varying(30) NOT NULL,
    cant_optima integer DEFAULT 20
);
 !   DROP TABLE public.utencilio_med;
       public         heap    postgres    false            J           2604    16598    bitacora id_cambio    DEFAULT     x   ALTER TABLE ONLY public.bitacora ALTER COLUMN id_cambio SET DEFAULT nextval('public.bitacora_id_cambio_seq'::regclass);
 A   ALTER TABLE public.bitacora ALTER COLUMN id_cambio DROP DEFAULT;
       public          postgres    false    223    222    223            �          0    16595    bitacora 
   TABLE DATA           |   COPY public.bitacora (id_cambio, id_historial_mod, fecha_modificacion, usuario, type_mod, valor_pre, valor_nue) FROM stdin;
    public          postgres    false    223   �<       �          0    16440 
   enfermedad 
   TABLE DATA           ;   COPY public.enfermedad (id_enfermedad, nombre) FROM stdin;
    public          postgres    false    214   UB       �          0    16443 	   historial 
   TABLE DATA           �   COPY public.historial (id_historial, fecha, herencia, tratamiento, evolucion, estado, comentario, id_lugar, id_paciente, id_medico, id_enfermedad) FROM stdin;
    public          postgres    false    215   sC       �          0    16448 
   inventario 
   TABLE DATA           a   COPY public.inventario (id_inventario, id_lugar, id_utencilio, cantidad, expiracion) FROM stdin;
    public          postgres    false    216   �F       �          0    16451    lugar 
   TABLE DATA           ?   COPY public.lugar (id_lugar, nombre, localizacion) FROM stdin;
    public          postgres    false    217   �H       �          0    16456    medico 
   TABLE DATA           n   COPY public.medico (id_medico, nombre, direccion, telefono, numcolegiado, especialidad, id_lugar) FROM stdin;
    public          postgres    false    218   K       �          0    16461    paciente 
   TABLE DATA           n   COPY public.paciente (id_paciente, nombre, masacorporal, altura, adicciones, telefono, direccion) FROM stdin;
    public          postgres    false    219   �M       �          0    16466    usuario 
   TABLE DATA           ?   COPY public.usuario (id_medico, usuario, password) FROM stdin;
    public          postgres    false    220   kQ       �          0    16469    utencilio_med 
   TABLE DATA           J   COPY public.utencilio_med (id_utencilio, nombre, cant_optima) FROM stdin;
    public          postgres    false    221   #S                  0    0    bitacora_id_cambio_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.bitacora_id_cambio_seq', 32, true);
          public          postgres    false    222            [           2606    16603    bitacora bitacora_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.bitacora
    ADD CONSTRAINT bitacora_pkey PRIMARY KEY (id_cambio);
 @   ALTER TABLE ONLY public.bitacora DROP CONSTRAINT bitacora_pkey;
       public            postgres    false    223            M           2606    16476    enfermedad enfermedad_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.enfermedad
    ADD CONSTRAINT enfermedad_pkey PRIMARY KEY (id_enfermedad);
 D   ALTER TABLE ONLY public.enfermedad DROP CONSTRAINT enfermedad_pkey;
       public            postgres    false    214            O           2606    16478    historial historial_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.historial
    ADD CONSTRAINT historial_pkey PRIMARY KEY (id_historial);
 B   ALTER TABLE ONLY public.historial DROP CONSTRAINT historial_pkey;
       public            postgres    false    215            Q           2606    16480    inventario inventario_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT inventario_pkey PRIMARY KEY (id_inventario);
 D   ALTER TABLE ONLY public.inventario DROP CONSTRAINT inventario_pkey;
       public            postgres    false    216            S           2606    16482    lugar lugar_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.lugar
    ADD CONSTRAINT lugar_pkey PRIMARY KEY (id_lugar);
 :   ALTER TABLE ONLY public.lugar DROP CONSTRAINT lugar_pkey;
       public            postgres    false    217            U           2606    16484    medico medico_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.medico
    ADD CONSTRAINT medico_pkey PRIMARY KEY (id_medico);
 <   ALTER TABLE ONLY public.medico DROP CONSTRAINT medico_pkey;
       public            postgres    false    218            W           2606    16486    paciente paciente_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.paciente
    ADD CONSTRAINT paciente_pkey PRIMARY KEY (id_paciente);
 @   ALTER TABLE ONLY public.paciente DROP CONSTRAINT paciente_pkey;
       public            postgres    false    219            Y           2606    16488     utencilio_med utencilio_med_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.utencilio_med
    ADD CONSTRAINT utencilio_med_pkey PRIMARY KEY (id_utencilio);
 J   ALTER TABLE ONLY public.utencilio_med DROP CONSTRAINT utencilio_med_pkey;
       public            postgres    false    221            e           2620    16573    historial historial_changes    TRIGGER     �   CREATE TRIGGER historial_changes AFTER INSERT OR DELETE OR UPDATE ON public.historial FOR EACH ROW EXECUTE FUNCTION public.historial_trigger();
 4   DROP TRIGGER historial_changes ON public.historial;
       public          postgres    false    215    235            d           2606    16604    bitacora bitacora_usuario_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.bitacora
    ADD CONSTRAINT bitacora_usuario_fkey FOREIGN KEY (usuario) REFERENCES public.medico(id_medico);
 H   ALTER TABLE ONLY public.bitacora DROP CONSTRAINT bitacora_usuario_fkey;
       public          postgres    false    223    4181    218            \           2606    16489 &   historial historial_id_enfermedad_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.historial
    ADD CONSTRAINT historial_id_enfermedad_fkey FOREIGN KEY (id_enfermedad) REFERENCES public.enfermedad(id_enfermedad);
 P   ALTER TABLE ONLY public.historial DROP CONSTRAINT historial_id_enfermedad_fkey;
       public          postgres    false    214    4173    215            ]           2606    16494 !   historial historial_id_lugar_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.historial
    ADD CONSTRAINT historial_id_lugar_fkey FOREIGN KEY (id_lugar) REFERENCES public.lugar(id_lugar);
 K   ALTER TABLE ONLY public.historial DROP CONSTRAINT historial_id_lugar_fkey;
       public          postgres    false    4179    215    217            ^           2606    16499 "   historial historial_id_medico_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.historial
    ADD CONSTRAINT historial_id_medico_fkey FOREIGN KEY (id_medico) REFERENCES public.medico(id_medico);
 L   ALTER TABLE ONLY public.historial DROP CONSTRAINT historial_id_medico_fkey;
       public          postgres    false    218    215    4181            _           2606    16504 $   historial historial_id_paciente_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.historial
    ADD CONSTRAINT historial_id_paciente_fkey FOREIGN KEY (id_paciente) REFERENCES public.paciente(id_paciente);
 N   ALTER TABLE ONLY public.historial DROP CONSTRAINT historial_id_paciente_fkey;
       public          postgres    false    219    215    4183            `           2606    16509 #   inventario inventario_id_lugar_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT inventario_id_lugar_fkey FOREIGN KEY (id_lugar) REFERENCES public.lugar(id_lugar);
 M   ALTER TABLE ONLY public.inventario DROP CONSTRAINT inventario_id_lugar_fkey;
       public          postgres    false    217    4179    216            a           2606    16514 '   inventario inventario_id_utencilio_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT inventario_id_utencilio_fkey FOREIGN KEY (id_utencilio) REFERENCES public.utencilio_med(id_utencilio);
 Q   ALTER TABLE ONLY public.inventario DROP CONSTRAINT inventario_id_utencilio_fkey;
       public          postgres    false    4185    216    221            b           2606    16519    medico medico_id_lugar_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.medico
    ADD CONSTRAINT medico_id_lugar_fkey FOREIGN KEY (id_lugar) REFERENCES public.lugar(id_lugar);
 E   ALTER TABLE ONLY public.medico DROP CONSTRAINT medico_id_lugar_fkey;
       public          postgres    false    4179    217    218            c           2606    16524    usuario usuario_id_medico_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_id_medico_fkey FOREIGN KEY (id_medico) REFERENCES public.medico(id_medico);
 H   ALTER TABLE ONLY public.usuario DROP CONSTRAINT usuario_id_medico_fkey;
       public          postgres    false    4181    218    220            �   �  x���n�F���S,|����ǒ�4I�lMZ�@�bE��-H��$5E��So���:��X&���֩0k�Kr����E:S6�ޜ��1�]�"�#�������b)�kq���T6���t!�J�������е4�HT;9Ub!+Y6�*�5�W��8mV��N�.�y?��l7+��J�k2���\�h��jX�ફB�U3k�d-���ڕ�ț�v՛��3U���kUV�(��"܎�b)�X�0��]Ϩ�nyaH0o�_g�F�L��S!�1;���YР���8�}~!��y��>w�G"<_7�;�ރ	汏c���6��sL��!����"�]4�*V��g�#C�d.�o��~H���;�E�E{���U�����2��{�H��D�lȨ�Z����g�bX�Cb/��K� <'���ŞxB�t�Cc~'
y�2L�yU:�h�r"�TgڠT��tU����ThT��K��VF���݈���jb�EZW͝p$�Va�����+�Y���,��ǵ>��	C !(�E��Z���v��-Dު���-�mF���)�Z]�/����6S��|��$�����`��q�o�gyo�GQ|S\�6dз���	vHt���N�+!�[!f�F>���)#׺<8�l%Ke��hPg|�w�ҾFFjQ��^�B[ QoN�*!= $f9c�bl��\�B�l�g}^S�=��m��lN�Q����P72�e��ŇۿzIQ����P$(�2ظ�p�.'**3����|�$���
�����G���IQ�b�a�����{�Q�l����q�UNi�^���zV`=xw%�G��ҝe-�D,����m'LX�p0��nb��<�瓅M6�gs���G��q`o!M�&EPTdU%.�s%�L�&E(�⮢���P�� $��&E�U�(ʋq�����)S�5VQ�!��(�z�xHx8P��aj'M��a�Wk�^dQ�]�C��~���Z������[:�������k[�a�5H�C�x���v���ZZ�����H�G�*P�+��7E�P��-��D��ڪƻ��˝ �~�uT;�Gm׎(ժPK�C�nz����}升'r�Q�0gj�߶�N}���ѧA��T�~)j�m
j�N�;Ap�Pc��+�K��G�wX�^{��^D��*��ߣ��k�=x?ʤ�(-�o>���ʥH������ �܏X`�>���ԫ�����M��Z|~smlmi�\�|�V�9��z�"�I��sɗ������Y�����{�J%1�/op�@n9���l��6�q�<�7}(���ƶ�o!P��ΖY3��,�Q[�wi��s��B��D��}�4a~�]ð-:�.������2�q�ޝ�f� ����      �     x�M�1N1E�S�oBH�U�HHDQ�8���۳���%E*:ڽ��P��������v�����P�)���P�l��T(f�#�A���9ԩ$.��6��.���#q���.�s��N�u��}ޭk�v��ųC[���DW���&�>K�(��g�\.�����]B��A�A��5�xJ�9�0��½'��'v���5-�U��������i/�p���Bz�-��-�E��%�X�	<���P
�H��2~n+��Ԑ/N�o7��g�t      �   |  x��V�n�8=��B?�B�,�9i�M��E�z�%�e!�ZR
��Q=�֫l%Z�I���)jޛ7o�\O9O�,a9�Sz�iA�e��r��:��q)�Z���ԭ�����XKW����˵p�ʵbWIz�t\�[XeqʉQq�ƒt�pF/���V�>��oE�*%�J�;|VK%[��WiU(CWF��T�(eщҀ�|?�.��9��V���c��M�
���Z5ҶR�>�SB7}��@�E` Y���r�J �U��������5��Gy`�]�Z< �P���
b�Sp`7*l;���@�����h���+ϵ�&���.��^	�L�;Y���W]a��Wu#���K��������(Rh�_k<�{����b���%of�{9�|��^�[�l՝�Y�%S�[�䴊�� �IҋEȿNuu���x/��c� :��T�Y���:bG�m�z	��s��!�\Ďf�H�|�L�G���(�����U���h�y���\�,Mx��yVy��hX����b�����{�y�l�#��A2`�}lJ<	�t��v�sR�u�B�n�e�����픴rk�P����#���3$��ƪ��!�ڔЯ��)�D<���$�PB%v
j��'�><��c�0���G�]�5�N l�%
̻n9��JmF4���Oj�(�v
����J�8��%�Dղt��CMv])�Ѫ|��l�J��GO Y��l�A��q��ŠS-����A�,�>�������)L�Y�-\[&���,�����ۇO�`K��ҕ����S�y�*�L's���T��3���hK� Џμ׫a�5����X����Nz�(���G��Ǉ�ʺ����D�ϔf��2���ap:��J��/�(��Q<      �   �  x�]TK%![�]�m�2�?����]D�lJd_O\����47Jl`��J�RH2lI���ܒ ��m��4�0.ĥQV ���i��p͠L=���+T� 2�1U�v��e�D�LRG-��u7
�ׇ1��ƃ��ԋM��	@�7��$߷��T�0纮�o�P�u�c0I���I
K������̃�'/Ow���a���8,�,bN��u2G��f�^��wO�Ñ�yXa�e�;�2t��!ރwAm�����٭����$���ޭk�׸J�kw�k�;�6�9�����㮃:ՄzwUÒ�t�?�?G!�|�v�{�b;i��bxK�6��G� ��k�z�	;�cE��ۻőԧ�?��3�|~�����z8a�U�Tv����"y�<�(2����"��cZ*֡�����ʞ��k�}m�c^��>�9ғ�F��	��|���Ox_ �z#w��!:{l��0��E�i�r�� ���c      �     x�u��n�0���S���v��c`$)�&b������hɠ����bQ��J��ُ�����XvB1���o]4'��µ�Z�"�-��խi��Dbr������p����O���7J�iMͰ���
$ر�0���uZ����nO��gݘ��-�/JF[P�T4��u�l�������>�v�Q�4��u��:ĉ��Y`b�T�$���n�`�aA�%E&�b���%�/M�Ϻ6�?Ԣ�Ð��X���X�N`qqA�Đ�\��������u�E>��Z&ZE0��{�C�IƎ��z�����JR�����:ζ6l=���R��)[Ba�R\0;��L'�.^J�1���k���Vs7�#�A&�*^�:���a�M_w�iF(�
*^qֿ���7�8�F0,kS:�z����ŌG?˃T\,����ϢXjI%́"�buMݳv�n��P�tV�pK����,� �).O#ނw��C�9q/�9W)��)0��v|�?���i'��Y �"��Z��s~'P�'�ڲzo7��?A�ѐ      �   �  x��U�n�@=�~�~��bX�9��(i�V��ec�.-k������CN�~���`"9��sɖy�y��؇[m���?k� C~�h���p¿����O�,kR����y�k�ѹ��J���bX�4ӵLX�>ےϵ]v_yz�g:��=�qd�J���>�Ɩy��pb�M�U��})�u�#	)���8�����
�V��7t�̴�ˊ���Ko�=�=vx;��A'\�����X7����{���^�w�PT�5���l]n��d�Ẵk�?[��E�,�{ξ����##�p���Ya�c�%pA��;ơ�ߑ"�����������"�Q2��}Ήqԋ�B��ǡc*����2�쐑�_��8�j�X	�kG��k@�!�<F	�ԏY:9�)���;�&�}�4���>,t�g�8ϸtr�;;xؔ���J�|.�ϳ�i�C��S��y8���aH]����`����u�����F��}�p0%��p$�|$��[���,�.d���Ѻ$g�v>�޹��d�6[��<���˽��*��X��ҕ��k��i��WW���!�����@�^P:��"�_��h�o�?˒K�4�ɣ�n&u���`�Y�{�<K�$��FW���fs��aU$Q�Z����^�}��ma7
      �   �  x�uV�n�8<7��`	jJ|�2Y�o�C�gF� Kg�X�or���|�~l�=���a���J���n�sUz�T	j���qjH�$4؜ܱ|r����տ�����	�=��?t��|��2�-�ۺ]���߸�.�5�	W�[�8�W��:�ݞ�K>}��p�|����m^�_5AK�b
>�
�$4����l�=���Z�c�P�}�?���~5{�6!	������!�JB;�&\9�f��N��qb~���U"�@�L�U�L�$�ȹX�Vp�|������ʴ2�A�+>2�TIh�j��GLĤ��5ܹ�w� �N��#uE����\Fj�u\���Q�j뼟�H�*	�@9'�\�k�n�ߑK@��y��*	p�[$b�Z��,8�j#�ٳ��;�U�R�p;[���j���VE�����ơ������hh��k��7՞������sxp��jb{KC�H���yoЮ����m��dp�[D�i����u__X�c��r��I^�.A�S��t��lv 2TCd�~Ӧ��Đ�2'�(������=��n}y %�����f4B�&a���p\�����)��8-}L*C�������
����
����,��%�Y	E�D�� ����h��tD#�A3����zp߽�&U��Z,� 1Ic1��B���������2�b|"�4щT�������=uoC�����3���<�x��1Q�q[=љ�t��&�.$.�\�%��	9f�j�L��.��E��
&Ȭn[�	�m\p�.�Ǆ9�<�mY;����[���.���E\�,L���w��X=��\�H�8O�-^��LX����W.�����s���^�.*�S�W�Tn�;�L�H�RV���������1����)      �   �  x�]��n�0���א�CEH�߂�u�6���P@[�B["�%��y�R�S�q����f�%��ϷN�`���3�#!�u�q/��=j(�o��D���p7k�r���P/�����H{��6�n]��ns�[�I��=^�i���x�� )4��]��t�Z*��ӛv�$��E� ���cV�|$еV��qS{�P�D^�MBo���O�=|�ƾ��3B)��C��{Nu)5�yb��!q?t�o��r��h�Gh�w�AL��Gv�9T�C#���_�I��(h��á�JZ��n�l䩗`��w\:�irqu�������W�ЩK'��zg,�V�K(v���+ߘ�x�op;���p0�{	��nv;��n°�t�-�0
+�{��@YH(�4�7c������uLX�22V������W̰      �   �  x�U�I��@E��)|���<,m��p�q��dCI�Q�j U2�&�,��X��������~�?�+����%�A����S��*�Wd,ȣ�uR8�c[��]���?U�V�?�CK�j{S��G��hr��Ab��+�z<���[�b�я(Z�Y�(�3�g��8�U�=H`�<�V� R��FyU��N�A��߽�h)�r�zc�
��8�k؋�*�i �J�t��D���M��qON���>[���q
/���ee����*.�вmH�r +8����5|S���VMOl��u�NK�kKj�u�vl�h�K�eX��To!��nM�x�N�DW��F�H���t�|�D��)���d	?d	X�*+�K�D`�S�����K�+�ayi{#�@,�+�s��L���=�K )d�����ѣ�]����K�LS9?�6]��n�·�5�����0�t�E�tBC���T��4������     