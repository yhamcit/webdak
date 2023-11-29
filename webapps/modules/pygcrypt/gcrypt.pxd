
cdef extern from "gcrypt.h":

    ctypedef unsigned int gpg_error_t
    ctypedef gpg_error_t gcry_error_t

    ctypedef struct gcry_sexp:
        pass
    ctypedef gcry_sexp* gcry_sexp_t

    ctypedef struct gcry_mpi:
        pass
    ctypedef gcry_mpi* gcry_mpi_t

    ctypedef struct gcry_mpi_point:
        pass 
    ctypedef gcry_mpi_point* gcry_mpi_point_t

    ctypedef struct gcry_context:
        pass 
    ctypedef gcry_context* gcry_ctx_t

    ctypedef struct gcry_md_handle:
        pass
    ctypedef gcry_md_handle *gcry_md_hd_t

    ctypedef struct gcry_buffer_t:
        size_t size
        size_t off
        size_t len
        void *data


    cdef enum gcry_md_algos: 
        GCRY_MD_NONE    = 0,
        GCRY_MD_MD5     = 1,
        GCRY_MD_SHA1    = 2,
        GCRY_MD_RMD160  = 3,
        GCRY_MD_MD2     = 5,
        GCRY_MD_TIGER   = 6, 
        GCRY_MD_HAVAL   = 7, 
        GCRY_MD_SHA256  = 8,
        GCRY_MD_SHA384  = 9,
        GCRY_MD_SHA512  = 10,
        GCRY_MD_SHA224  = 11,

        GCRY_MD_MD4           = 301,
        GCRY_MD_CRC32         = 302,
        GCRY_MD_CRC32_RFC1510 = 303,
        GCRY_MD_CRC24_RFC2440 = 304,
        GCRY_MD_WHIRLPOOL     = 305,
        GCRY_MD_TIGER1        = 306, 
        GCRY_MD_TIGER2        = 307, 
        GCRY_MD_GOSTR3411_94  = 308, 
        GCRY_MD_STRIBOG256    = 309, 
        GCRY_MD_STRIBOG512    = 310, 
        GCRY_MD_GOSTR3411_CP  = 311, 
        GCRY_MD_SHA3_224      = 312,
        GCRY_MD_SHA3_256      = 313,
        GCRY_MD_SHA3_384      = 314,
        GCRY_MD_SHA3_512      = 315,
        GCRY_MD_SHAKE128      = 316,
        GCRY_MD_SHAKE256      = 317,
        GCRY_MD_BLAKE2B_512   = 318,
        GCRY_MD_BLAKE2B_384   = 319,
        GCRY_MD_BLAKE2B_256   = 320,
        GCRY_MD_BLAKE2B_160   = 321,
        GCRY_MD_BLAKE2S_256   = 322,
        GCRY_MD_BLAKE2S_224   = 323,
        GCRY_MD_BLAKE2S_160   = 324,
        GCRY_MD_BLAKE2S_128   = 325,
        GCRY_MD_SM3           = 326,
        GCRY_MD_SHA512_256    = 327,
        GCRY_MD_SHA512_224    = 328


    cdef enum gcry_mpi_format:
        GCRYMPI_FMT_NONE= 0,
        GCRYMPI_FMT_STD = 1,
        GCRYMPI_FMT_PGP = 2,
        GCRYMPI_FMT_SSH = 3,
        GCRYMPI_FMT_HEX = 4,
        GCRYMPI_FMT_USG = 5,
        GCRYMPI_FMT_OPAQUE = 8

    cdef enum gcry_sexp_format:
        GCRYSEXP_FMT_DEFAULT   = 0,
        GCRYSEXP_FMT_CANON     = 1,
        GCRYSEXP_FMT_BASE64    = 2,
        GCRYSEXP_FMT_ADVANCED  = 3

    cdef enum gcry_ecc_ctx_get:
        GCRY_PK_GET_PUBKEY  = 1,
        GCRY_PK_GET_SECKEY  = 2


    const char *gcry_strerror (gcry_error_t err)


    void gcry_ctx_release (gcry_ctx_t ctx)


    cdef gcry_error_t gcry_pk_encrypt (gcry_sexp_t *result, gcry_sexp_t data, gcry_sexp_t pkey)

    cdef gcry_error_t gcry_pk_decrypt (gcry_sexp_t *result, gcry_sexp_t data, gcry_sexp_t skey)
    

    gcry_error_t gcry_pk_sign (gcry_sexp_t *result, gcry_sexp_t data, gcry_sexp_t skey)

    gcry_error_t gcry_pk_verify (gcry_sexp_t sig, gcry_sexp_t data, gcry_sexp_t pkey)


    gcry_error_t gcry_sexp_new (gcry_sexp_t *retsexp, const void *buffer, size_t length, int autodetect)

    gcry_error_t gcry_pubkey_get_sexp (gcry_sexp_t *r_sexp, int mode, gcry_ctx_t ctx)


    int gcry_sexp_length (const gcry_sexp_t list)

    void gcry_sexp_release (gcry_sexp_t sexp)


    gcry_error_t gcry_sexp_create (gcry_sexp_t *retsexp, void *buffer, size_t length, int autodetect, void (*freefnc) (void *))

    gcry_error_t gcry_sexp_sscan (gcry_sexp_t *retsexp, size_t *erroff, const char *buffer, size_t length)

    gcry_error_t gcry_sexp_build (gcry_sexp_t *retsexp, size_t *erroff, const char *format, ...)

    gcry_error_t gcry_sexp_build_array (gcry_sexp_t *retsexp, size_t *erroff, const char *format, void **arg_list)




    gcry_sexp_t gcry_sexp_find_token (gcry_sexp_t list, const char *tok, size_t toklen)

    size_t gcry_sexp_sprint (gcry_sexp_t sexp, int mode, void *buffer, size_t maxlength)

    gcry_sexp_t gcry_sexp_car (const gcry_sexp_t list)

    gcry_sexp_t gcry_sexp_cdr (const gcry_sexp_t list)

    void gcry_sexp_dump (const gcry_sexp_t a)

    gcry_sexp_t gcry_sexp_nth (const gcry_sexp_t list, int number)

    char *gcry_sexp_nth_string (gcry_sexp_t list, int number)

    const char *gcry_sexp_nth_data (const gcry_sexp_t list, int number, size_t *datalen)

    void * gcry_sexp_nth_buffer (const gcry_sexp_t list, int number, size_t *rlength)


    gcry_mpi_t gcry_sexp_nth_mpi (gcry_sexp_t list, int number, int mpifmt)


    void  gcry_free (void *a)


    # """ 
    # large numbers are called MPIs (multi-precision-integers). 
    # Public key cryptography is based on mathematics with large numbers. These functions are exposed 
    # """
    gcry_mpi_t gcry_mpi_new (unsigned int nbits)

    void gcry_mpi_release (gcry_mpi_t a)

    gcry_error_t gcry_mpi_print (gcry_mpi_format format, unsigned char *buffer, size_t buflen, size_t *nwritten, const gcry_mpi_t a)

    gcry_error_t gcry_mpi_aprint (gcry_mpi_format format, unsigned char **buffer, size_t *nbytes, const gcry_mpi_t a)


    # """ 
    # Points in MPI coordinate system 
    # projective coordinates from a Point on each axis of 3-Dimensionality system are MPI.
    # Currently Only ECC functions implement context. Use gcry_mpi_ec_new to create one.
    # """

    gpg_error_t gcry_mpi_ec_new (gcry_ctx_t *r_ctx, gcry_sexp_t keyparam, const char *curvename)

    void gcry_ctx_release (gcry_ctx_t ctx)

    void gcry_mpi_point_release (gcry_mpi_point_t point)

    gcry_mpi_point_t gcry_mpi_ec_get_point (const char *name, gcry_ctx_t ctx, int copy)

    void gcry_mpi_point_get (gcry_mpi_t x, gcry_mpi_t y, gcry_mpi_t z, gcry_mpi_point_t point)

    int gcry_mpi_ec_get_affine ( gcry_mpi_t x, gcry_mpi_t y, gcry_mpi_point_t point, gcry_ctx_t ctx)


    gpg_error_t gcry_mpi_ec_set_point (const char *name,  gcry_ctx_t ctx)
    
    gpg_error_t gcry_mpi_ec_set_mpi (const char *name, gcry_mpi_t newvalue, gcry_ctx_t ctx)

    gcry_mpi_t gcry_mpi_ec_get_mpi (const char *name, gcry_ctx_t ctx, int copy)



    const char *gcry_strerror (gcry_error_t err)

    const char *gcry_strsource (gcry_error_t err)


    const char *gcry_check_version (const char *req_version)



    gcry_error_t gcry_md_open (gcry_md_hd_t *h, int algo, unsigned int flags)

    void gcry_md_close (gcry_md_hd_t h)

    void gcry_md_reset (gcry_md_hd_t h)

    unsigned char * gcry_md_read (gcry_md_hd_t h, int algo)

    void gcry_md_write (gcry_md_hd_t h, const void *buffer, size_t length)


    gcry_error_t gcry_md_open (gcry_md_hd_t *h, int algo, unsigned int flags)

    void gcry_md_close (gcry_md_hd_t hd)

    void gcry_md_write (gcry_md_hd_t hd, const void *buffer, size_t length)

    unsigned char *gcry_md_read (gcry_md_hd_t hd, int algo)

    gpg_error_t gcry_md_hash_buffers (int algo, unsigned int flags, void *digest, const gcry_buffer_t *iov, int iovcnt)

    void gcry_md_hash_buffer (int algo, void *digest, const void *buffer, size_t length)

    unsigned int gcry_md_get_algo_dlen (int algo)

    const char *gcry_md_algo_name (int algo)