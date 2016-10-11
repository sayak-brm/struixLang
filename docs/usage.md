## Usage:

To run the default shell for **struixLang**, run the `repl.py` file under Python 3.

The interpreter can also be imported from within other Python programs.

    import struixTerp

However the interpreter by itself does not form the language. To import the primitives do:

    import struixPrimitives

Then create a new instance of the interpretor:

    terp = struixTerp.Terp()

Add the primitives to it:

    struixPrimitives.AddWords(terp)

And give the interpreter a string of struixLang code to run:

    terp.run("""
             var a
             a 10 store
             "Hello, World!"
             print 2 times
             """)

However some potentially dangerous operations are enabled only on passing the following to `struixPrimitives.AddWords()`:

    struixPrimitives.AddWords(terp, terp.ENABLE_UNSAFE_OPERATIONS)